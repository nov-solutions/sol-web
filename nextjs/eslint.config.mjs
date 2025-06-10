import { FlatCompat } from '@eslint/eslintrc'

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
})

const eslintConfig = [
  ...compat.config({
    extends: [
      'next/core-web-vitals', 'next/typescript'
    ],
    settings: {
      next: {
        rootDir: 'nextjs/',
      },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@next/no-html-link-for-pages': 'off',
      // generally a good idea to keep the rule below on, but turning this rule off for now
      // prevents immediate errors and having to specify width and height for images without testing
      '@next/next/no-img-element': 'off',
    },
  }),
];

export default eslintConfig;
