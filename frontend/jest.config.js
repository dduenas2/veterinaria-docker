
module.exports = {

  testEnvironment: 'jsdom',

  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],

  testMatch: ['**/__tests__/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],

  moduleNameMapper: {

    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',

  },

  collectCoverageFrom: [

    'src/**/*.{js,jsx}',

    '!src/index.js',

    '!src/reportWebVitals.js',

  ],

  coverageThreshold: {

    global: {

      branches: 50,

      functions: 50,

      lines: 50,

      statements: 50

    }

  }

};

