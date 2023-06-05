
export function useYAPI(){
    if (!connected){
        const script = document.createElement('script');
        script.src =  state.YAPI_url;
        document.head.appendChild(script);
        setTimeout(()=>{commit("connected",true)}, 150);

    }
}