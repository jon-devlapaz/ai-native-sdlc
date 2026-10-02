// Four native judge calls through promptfoo; fixed saved answers, no writer calls.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const runtime = process.env.STAGE01_EVAL_RUNTIME;
if (!runtime) throw new Error('Set STAGE01_EVAL_RUNTIME to the existing isolated installation.');
for (const name of Object.keys(process.env)) {
  if (/^(ANTHROPIC_|OPENAI_|CODEX_API_|CLAUDE_CODE_USE_|CLAUDE_CODE_OAUTH_TOKEN)/.test(name)) delete process.env[name];
}
process.env.PROMPTFOO_DISABLE_TELEMETRY = '1';
process.env.PROMPTFOO_CACHE_ENABLED = 'false';
process.env.PROMPTFOO_CONFIG_DIR = path.join(runtime, 'local-state');
process.chdir(runtime);
const { evaluate, loadApiProvider } = await import(pathToFileURL(path.join(runtime, 'node_modules/promptfoo/dist/src/index.js')));
const configPath = path.join(here, 'calibration-v2.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const replay = process.env.STAGE01_CALIBRATION_REPLAY;
const output = path.join(runtime, replay ? 'calibration-v2-replay' : 'calibration-v2');
if (fs.existsSync(output)) throw new Error('Calibration evidence already exists; refusing to overwrite.');
fs.mkdirSync(output);
fs.copyFileSync(configPath, path.join(output, 'frozen-config.json'));
fs.copyFileSync(path.join(here, 'owner-labels.json'), path.join(output, 'owner-labels.json'));
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
fs.writeFileSync(path.join(output, 'inputs.json'), JSON.stringify({
  configSha256: sha(configPath), ownerLabelsSha256: sha(path.join(here, 'owner-labels.json')),
  runnerSha256: sha(fileURLToPath(import.meta.url)), plannedModelTurns: replay ? 0 : 4,
  replaySource: replay || null,
  writerCalls: 0, startedAt: new Date().toISOString(),
}, null, 2));
const stop = new AbortController();
process.on('SIGTERM', () => stop.abort());
process.on('SIGINT', () => stop.abort());
let calls = 0;
const spec = config.providers[0];
spec.config.working_dir = path.join(runtime, 'empty-judge-workspace');
const saved = new Map();
if (replay) {
  for (let number = 1; number <= 4; number++) {
    const file = path.join(replay, `call-${number}.json`);
    const receipt = JSON.parse(fs.readFileSync(file, 'utf8'));
    saved.set(receipt.prompt, { file, response: receipt.response });
  }
}
const judge = replay ? {
  id: () => 'captured-judge-response',
  callApi: async (prompt) => {
    const receipt = saved.get(prompt);
    if (!receipt) throw new Error('No saved response for this exact grading prompt.');
    const number = [...saved.keys()].indexOf(prompt) + 1;
    fs.writeFileSync(path.join(output, `reused-call-${number}.json`), JSON.stringify(receipt, null, 2));
    return { output: receipt.response.output, cached: true,
      tokenUsage: { total: 0, prompt: 0, completion: 0, numRequests: 0 },
      metadata: { replaySource: receipt.file, newModelCalls: 0 } };
  },
} : await loadApiProvider(spec.id, { options: spec, basePath: runtime });
const nativeCall = judge.callApi.bind(judge);
judge.callApi = async (prompt, context, options = {}) => {
  if (stop.signal.aborted) throw new Error('Calibration stopped.');
  if (prompt !== context.vars.judgingPrompt || !prompt.includes('ORIGINAL REQUEST:\nUser request:')) {
    stop.abort(); throw new Error('Rendered grading prompt differs from the frozen complete prompt.');
  }
  const number = replay ? 0 : ++calls;
  if (calls > 4) { stop.abort(); throw new Error('Four-call limit exceeded.'); }
  const timeout = new AbortController();
  const timer = setTimeout(() => timeout.abort(), 120000);
  const abortSignal = AbortSignal.any([stop.signal, timeout.signal, ...(options.abortSignal ? [options.abortSignal] : [])]);
  console.log(replay ? 'Replaying a captured judge response' : `Judge call ${number}/4`);
  try {
    const response = await nativeCall(prompt, context, { ...options, abortSignal });
    if (!replay) fs.writeFileSync(path.join(output, `call-${number}.json`), JSON.stringify({
      number, provider: spec, prompt, response, completedAt: new Date().toISOString(),
    }, null, 2));
    if (response.error || !response.output || timeout.signal.aborted) {
      stop.abort(); throw new Error(response.error || 'Missing or timed-out answer.');
    }
    return response;
  } catch (error) {
    stop.abort();
    fs.writeFileSync(path.join(output, `call-${number}-error.json`), JSON.stringify({ number, error: String(error), prompt }, null, 2));
    throw error;
  } finally { clearTimeout(timer); }
};
const record = await evaluate({ ...config, providers: [judge] }, { ...config.evaluateOptions, abortSignal: stop.signal });
fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(await record.toResultsFile(), null, 2));
fs.writeFileSync(path.join(output, 'completion.json'), JSON.stringify({
  evalId: record.id, modelCalls: calls, replayedJudgments: replay ? 4 : 0,
  aborted: stop.signal.aborted, completedAt: new Date().toISOString(),
}, null, 2));
console.log(JSON.stringify({ evalId: record.id, calls, aborted: stop.signal.aborted }));
if (stop.signal.aborted) process.exitCode = 1;
