import commonjs from "@rollup/plugin-commonjs";
import dts from "rollup-plugin-dts";
import esbuild from "rollup-plugin-esbuild";
import nodeExternals from "rollup-plugin-node-externals";
import nodeResolve from "@rollup/plugin-node-resolve";
import postcss from "rollup-plugin-postcss";
import terser from "@rollup/plugin-terser";
import replace from "@rollup/plugin-replace";

import { readFileSync } from "fs";

const packageJson = JSON.parse(readFileSync("package.json", "utf-8"));

export default [
  {
    input: "src/index.ts",
    output: [
      {
        file: "dist/cjs/index.js",
        format: "cjs",
        sourcemap: true,
      },
      {
        file: "dist/esm/index.js",
        format: "esm",
        sourcemap: true,
      },
    ],
    plugins: [
      replace({
        "process.env.CURRENT_VERSION": JSON.stringify(packageJson.version),
        "process.env.BUILD_TIME": JSON.stringify(new Date().toISOString()),
      }),
      nodeExternals(),
      nodeResolve(),
      commonjs(),
      esbuild({ tsconfig: "./tsconfig.json" }),
      postcss({ modules: true }),
      terser(),
    ],
  },
  {
    input: "src/index.ts",
    output: [
      {
        file: "dist/index.d.ts",
        format: "esm",
      },
    ],
    plugins: [dts({ tsconfig: "./tsconfig.json" })],
  },
];
