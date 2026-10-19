import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],build:{outDir:'dist-rig-v2',rollupOptions:{input:'rig-v2.html'}},server:{host:'127.0.0.1',port:5190,strictPort:true},preview:{host:'127.0.0.1',port:5190,strictPort:true}});
