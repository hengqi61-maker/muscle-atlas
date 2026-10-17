import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'chrome-diagnostic.spec.ts',
 use:{baseURL:'http://127.0.0.1:5175',launchOptions:{channel:'chrome'},viewport:{width:1440,height:1000}},
 webServer:{command:'npm run dev -- --mode test --port 5175 --strictPort',url:'http://127.0.0.1:5175',reuseExistingServer:false},workers:1});
