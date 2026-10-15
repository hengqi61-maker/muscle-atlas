import {Component,type ReactNode} from 'react';
export class SceneBoundary extends Component<{children:ReactNode},{error:string|null}>{
 state={error:null as string|null};
 static getDerivedStateFromError(error:Error){return {error:error.message};}
 render(){return this.state.error?<div role="alert" className="scene-error">3D 场景加载失败。请检查本地模型文件并刷新。<small>{this.state.error}</small></div>:this.props.children;}
}
