module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    "plugin:@typescript-eslint/eslint-recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:import/recommended",
  ],
  plugins: ["@typescript-eslint", "import", "prettier"],
  rules: {
    "newline-per-chained-call": "off",
  },
  parserOptions: {
    project: "./tsconfig.json",
  },
  ignorePatterns: [],
  overrides: [
    {
      // The files listed below are part of the build process, so they will be using packages that are listed
      // under devDependences and/or peerDependencies, so we need to be lenient with the import/no-extraneous-dependencies
      files: [".eslintrc.js", "rollup.config.mjs"],
      rules: {
        "import/no-extraneous-dependencies": ["error", { peerDependencies: true, devDependencies: true }],
      },
    },
  ],
};
