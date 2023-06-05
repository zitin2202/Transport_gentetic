import { useStore } from 'vuex';
import {watch} from "vue";

export function useWhenMapLoad(functionBody) {
    const store = useStore();

    // Используйте store для доступа к состояниям, действиям, геттерам и мутациям


    if ( store.state.MainMapModule.MainMap!=null){
        functionBody()
    }
    else {
        watch(
            () => store.state.MainMapModule.MainMap,
            (newValue) => {
                if (newValue!==null) {
                    functionBody()
                }
            },
            {once: true}
        );

    }


    return {
    };
}