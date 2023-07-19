module.exports = {
	root: true,
	extends: ['eslint:recommended', 'plugin:svelte/recommended', 'plugin:@typescript-eslint/recommended', 'prettier'],
    parser: '@typescript-eslint/parser',
    plugins: ['@typescript-eslint'],
	parserOptions: {
		sourceType: 'module',
		ecmaVersion: 2020,
		extraFileExtensions: ['.svelte']
	},
	env: {
		browser: true,
		es2017: true,
		node: true
    },
    rules: {
        "@typescript-eslint/no-explicit-any": "error",
    }
};
