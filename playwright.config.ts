import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'tests/browser',use:{baseURL:'http://127.0.0.1:5175',viewport:{width:1440,height:1000},launchOptions:{channel:'chrome'}},webServer:{command:'npm run dev -- --mode test --port 5175 --strictPort',url:'http://127.0.0.1:5175',reuseExistingServer:false},workers:1});
