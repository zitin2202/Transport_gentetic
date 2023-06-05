
export const MainMapModule = {
    namespaced: true,
    state:() => ({
        MainMap :null
    }),
    getters: {
    },
    mutations:{
        setMap(state, map) {
            state.MainMap = map;

        }
    },
    actions:{

    },
}