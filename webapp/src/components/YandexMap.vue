<template>
  <div>
    <div ref="map" className="map">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { ref, watch} from 'vue';
import {useStore} from 'vuex';

export default {
  name: 'yandex-map',
  props: {
    center: {
      type: Array,
      required: true
    },
    zoom: {
      type: Number,
      default: 10
    }
  },

  setup(props) {
    const map = ref(null);
    // Инициализация карты
    let store = useStore();
    let mapInstance = null;
    // Инициализация карты
    const initializeMap = () => {
      if (window.ymaps && window.ymaps.Map) {
        mapInstance = new window.ymaps.Map(map.value, {
          center: props.center,
          zoom: props.zoom,
          controls: []
        },);
        store.commit("MainMapModule/setMap", mapInstance);


      }
      // else {
      //   console.error('Ошибка загрузки API Яндекс.Карт');
      //   setTimeout(initializeMap, 100);
      //
      // }
    };

    if (store.state.YAPIModule.connected){
      initializeMap(); // Ваш метод initializeMap()
    }
    else {
      watch(
          () => store.state.YAPIModule.connected,
          (newValue) => {
            if (newValue) {
              initializeMap(); // Ваш метод initializeMap()
            }
          }
      );
    }


    return {
      map,

      store,
    };

  },


};
</script>

<style scoped>
.map {
  width: 100%;
  height: 400px;
  margin-top: 40px;
  margin-bottom: 40px;

}
</style>