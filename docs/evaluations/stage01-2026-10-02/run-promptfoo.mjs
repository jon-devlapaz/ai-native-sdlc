// Promptfoo runs the comparison. This wrapper preserves raw calls and stops on errors.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const runtime = process.env.STAGE01_EVAL_RUNTIME;
if (!runtime) throw new Error('Set STAGE01_EVAL_RUNTIME to the isolated promptfoo installation.');
const require = createRequire(path.join(runtime, 'package.json'));
// Only subscription logins are in scope. Do not inherit API credentials or alternate endpoints.
for (const name of Object.keys(process.env)) {
  if (/^(ANTHROPIC_|OPENAI_|CODEX_API_|CLAUDE_CODE_USE_|CLAUDE_CODE_OAUTH_TOKEN)/.test(name)) delete process.env[name];
}
process.env.PROMPTFOO_DISABLE_TELEMETRY = '1';
process.env.PROMPTFOO_CACHE_ENABLED = 'false';
process.env.PROMPTFOO_CONFIG_DIR = path.join(runtime, 'local-state');
// The optional SDK loader resolves packages from the process working directory.
process.chdir(runtime);
const { evaluate, loadApiProvider } = await import(pathToFileURL(path.join(runtime, 'node_modules/promptfoo/dist/src/index.js')));
const configPath = path.join(here, 'promptfooconfig.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const outputDir = path.join(runtime, process.env.STAGE01_EVAL_RUN || 'run-1');
if (fs.existsSync(outputDir)) throw new Error('Output directory already exists; preserve it rather than overwriting trials.');
fs.mkdirSync(outputDir, { recursive: true });
fs.mkdirSync(path.join(runtime, 'empty-judge-workspace'), { recursive: true });
fs.copyFileSync(configPath, path.join(outputDir, 'frozen-config.json'));
fs.copyFileSync(path.join(here, 'long/evals/tasks.jsonl'), path.join(outputDir, 'frozen-tasks.jsonl'));
const digest = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
fs.writeFileSync(path.join(outputDir, 'inputs.json'), JSON.stringify({
  configSha256: digest(configPath), tasksSha256: digest(path.join(here, 'long/evals/tasks.jsonl')),
  runnerSha256: digest(fileURLToPath(import.meta.url)), startedAt: new Date().toISOString(),
  promptfooVersion: JSON.parse(fs.readFileSync(path.join(runtime, 'node_modules/promptfoo/package.json'), 'utf8')).version,
  plannedJudgeCalls: 12,
  reusedTargetsFrom: process.env.STAGE01_REUSE_TARGETS || null,
}, null, 2));

const stop = new AbortController();
// SDK signal handlers can consume SIGTERM; bind it to the evaluator's abort signal.
process.on('SIGTERM', () => stop.abort());
process.on('SIGINT', () => stop.abort());
let count = 0;
const reused = new Map();
if (process.env.STAGE01_REUSE_TARGETS) {
  for (const file of fs.readdirSync(process.env.STAGE01_REUSE_TARGETS).filter((s) => /^call-\d+-target\.json$/.test(s))) {
    const receipt = JSON.parse(fs.readFileSync(path.join(process.env.STAGE01_REUSE_TARGETS, file), 'utf8'));
    if (receipt.response.output && !receipt.response.error) reused.set(receipt.prompt, { file, response: receipt.response });
  }
  if (reused.size < 1 || reused.size > 12) throw new Error('Unexpected retained target count.');
}
const callLimit = 24 - reused.size;
const inputReceipt = JSON.parse(fs.readFileSync(path.join(outputDir, 'inputs.json'), 'utf8'));
Object.assign(inputReceipt, { plannedCalls: callLimit, plannedTargetCalls: 12 - reused.size, reusedTargets: reused.size });
fs.writeFileSync(path.join(outputDir, 'inputs.json'), JSON.stringify(inputReceipt, null, 2));
async function recordingProvider(spec, role) {
  const native = await loadApiProvider(spec.id, { options: spec, basePath: runtime });
  const call = native.callApi.bind(native);
  native.callApi = async (prompt, context, options = {}) => {
    if (stop.signal.aborted) throw new Error('Pilot stopped after an earlier call error.');
    if (role === 'judge' && !prompt.includes('ORIGINAL REQUEST:\nUser request:')) {
      stop.abort(); throw new Error('Rendered judge prompt is missing the original request; no model call made.');
    }
    if (role === 'target' && reused.has(prompt)) {
      const receipt = reused.get(prompt);
      fs.writeFileSync(path.join(outputDir, `reused-${receipt.file}`), JSON.stringify({ prompt, ...receipt }, null, 2));
      console.log(`Reused target answer: ${receipt.file}`);
      return receipt.response;
    }
    const number = ++count;
    if (number > callLimit) { stop.abort(); throw new Error('Planned call limit exceeded.'); }
    const startedAt = new Date().toISOString();
    const timer = new AbortController();
    const timeout = setTimeout(() => timer.abort(), 120000);
    const abortSignal = AbortSignal.any([stop.signal, timer.signal, ...(options.abortSignal ? [options.abortSignal] : [])]);
    console.log(`Call ${number}/${callLimit}: ${role}`);
    try {
      const response = await call(prompt, context, { ...options, abortSignal });
      fs.writeFileSync(path.join(outputDir, `call-${String(number).padStart(2, '0')}-${role}.json`), JSON.stringify({
        number, role, provider: spec, startedAt, completedAt: new Date().toISOString(), prompt, response,
      }, null, 2));
      if (response.error || timer.signal.aborted || !response.output) {
        stop.abort();
        throw new Error(response.error || 'Call timed out or returned no answer.');
      }
      return response;
    } catch (error) {
      stop.abort();
      fs.writeFileSync(path.join(outputDir, `call-${String(number).padStart(2, '0')}-${role}-error.json`), JSON.stringify({
        number, role, startedAt, completedAt: new Date().toISOString(), error: String(error), prompt,
      }, null, 2));
      throw error;
    } finally { clearTimeout(timeout); }
  };
  return native;
}

const target = await recordingProvider(config.providers[0], 'target');
const judgeSpec = config.defaultTest.options.provider;
judgeSpec.config.working_dir = path.join(runtime, 'empty-judge-workspace');
const judge = await recordingProvider(judgeSpec, 'judge');
const suite = { ...config, providers: [target], defaultTest: {
  ...config.defaultTest, options: { ...config.defaultTest.options, provider: judge },
}, sharing: false, writeLatestResults: true };
const record = await evaluate(suite, { ...config.evaluateOptions, abortSignal: stop.signal });
const results = await record.toResultsFile();
fs.writeFileSync(path.join(outputDir, 'results.json'), JSON.stringify(results, null, 2));
fs.writeFileSync(path.join(outputDir, 'completion.json'), JSON.stringify({
  evalId: record.id, calls: count, aborted: stop.signal.aborted, completedAt: new Date().toISOString(),
}, null, 2));
console.log(JSON.stringify({ evalId: record.id, calls: count, aborted: stop.signal.aborted }));
if (stop.signal.aborted) process.exitCode = 1;
