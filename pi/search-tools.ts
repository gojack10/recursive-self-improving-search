import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

function call(name: string, args: unknown): Promise<string> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.env.RSIS_PYTHON ?? "python3", ["-m", "rsis.pi_tool", name], { cwd: process.env.RSIS_ROOT });
    let output = "", error = "";
    child.stdout.on("data", (data) => (output += data));
    child.stderr.on("data", (data) => (error += data));
    child.on("error", reject);
    child.on("close", (code) => code === 0 ? resolve(output) : reject(new Error(error.slice(-500) || `exit ${code}`)));
    child.stdin.end(JSON.stringify(args));
  });
}

export default function (pi: ExtensionAPI) {
  // One writer per agent state file, including on Windows where fcntl is unavailable.
  let pending: Promise<unknown> = Promise.resolve();
  const schemas = JSON.parse(readFileSync(process.env.RSIS_TOOLS!, "utf8"));
  for (const schema of schemas) {
    pi.registerTool({
      name: schema.name,
      label: schema.name,
      description: schema.description,
      parameters: Type.Unsafe(schema.parameters),
      async execute(_id, params) {
        const operation = pending.then(() => call(schema.name, params));
        pending = operation.catch(() => undefined);
        const text = await operation;
        const done = ["submit", "propose"].includes(schema.name) && JSON.parse(text).ok === true;
        return { content: [{ type: "text" as const, text }], details: {}, terminate: done };
      },
    });
  }
}
