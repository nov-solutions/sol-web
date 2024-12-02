const eslint = require('@eslint/js');
const tseslint = require('typescript-eslint');

module.exports = tseslint.config(
    eslint.configs.recommended,
    ...tseslint.configs.recommended,
    {
        ignores: ['django/**', 'nextjs/.next/**', 'package.json', '**/*.config.js', '**/.cache/**',],
    }
);
