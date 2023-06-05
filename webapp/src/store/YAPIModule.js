
export const YAPIModule = {
    namespaced: true,
    state:() => ({
        API_key:"1f2568c2-9262-4943-ad8f-fb28a2c7b561",
        version:2.1,
        connected:false,
        YAPI_url:"https://api-maps.yandex.ru/2.1/?apikey=1f2568c2-9262-4943-ad8f-fb28a2c7b561&lang=ru_RU",
    }),
    getters:{


    },
    mutations:{

    },
    actions:{
        CheckConnectAPI({state}){
            if (!state.connected){
                // const script = document.createElement('script');
                // script.src =  state.YAPI_url;
                // document.head.appendChild(script);
                let interval = setInterval(()=>{
                    if (window.ymaps && window.ymaps.Map) {
                        state.connected = true;
                        clearInterval(interval);
                    }
                }, 100);

            }
        }

    },
}