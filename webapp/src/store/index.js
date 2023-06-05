import {createStore} from 'vuex';
import {YAPIModule} from "@/store/YAPIModule";
import {MainMapModule} from "@/store/MainMapModule";
import {GlobalSettingModule} from "@/store/GlobalSettingModule";

export default createStore({

    modules:{
        YAPIModule: YAPIModule,
        MainMapModule: MainMapModule,
        GlobalSettingModule:GlobalSettingModule,
    }

})