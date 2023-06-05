
export const GlobalSettingModule = {
    namespaced: true,
    state:() => ({
        isInputDisabled :false
    }),
    getters: {
    },
    mutations:{
        setIsInputDisabled(state, value) {
            state.isInputDisabled = value;
        }
    },
    actions:{

    },
}