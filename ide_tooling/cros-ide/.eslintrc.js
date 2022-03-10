// Copyright 2022 The Chromium OS Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': [
    'google',
  ],
  'parser': '@typescript-eslint/parser',
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module',
  },
  'plugins': [
    '@typescript-eslint',
  ],
  'rules': {
    // These rules should be enabled but are temporary disabled until the
    // violations are removed from the code.
    'require-jsdoc': 0,
    'arrow-parens': 0,
    'max-len': ['error', {code: 100}],
    'no-throw-literal': 0,
    'no-invalid-this': 0,
    'valid-jsdoc': 0, // has been deprecated in ESLint v5.10.0.
  },
};
