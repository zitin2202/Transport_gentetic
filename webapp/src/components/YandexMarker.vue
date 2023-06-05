<template>
<div style="display: none">

</div>
</template>

<script>

import {useStore} from "vuex";
import {watch} from "vue";

export default {
  name: "yandex-marker",
  props:{
    markerNumber:{
      type:Number,
      required:true
    },
    coords:{
      type:Object,
      required:true
    },
    object:{
      type:Object,
      required:true
    },

    type:{
      type:String,
      required:true
    },

  },

  methods:{
  }
  ,
  setup(props,{emit}){
    let store = useStore();

    const updateMarkerObject = (object) => {
      emit('updateMarkerObjectEvent',object)
    }


    const updateMarker = () => {
      let map = store.state.MainMapModule.MainMap.__v_raw
      if (props.object!=null){
        map.geoObjects.remove(props.object.__v_raw)
        updateMarkerObject(null)
      }

      if (props.coords!=null){
        let fontSize = 19 - props.markerNumber.toString().length*3;
        let MyIconContentLayout = window.ymaps.templateLayoutFactory.createClass(
            '<div style="color: #000000; margin-left: 17px;  margin-top: 11px; width: 27px; text-align: center; font-weight: bold; font-size: '+fontSize+'px ">$[properties.iconContent]</div>'
        );
        let marker = new window.ymaps.Placemark(props.coords,{
              hintContent: 'Собственный значок метки с контентом',
              balloonContent: 'А эта — новогодняя',
              iconContent: props.markerNumber,
            },
            {
              iconImageHref: require('@/assets/' +props.type + 'Icon.png'),
              iconImageSize: [60, 60],
              iconOffset: [-30, -55],
              iconLayout: 'default#imageWithContent',
              iconContentLayout: MyIconContentLayout,

            }
        );
        map.geoObjects.add(marker);
        updateMarkerObject(marker)
        map.setCenter(props.coords, 15)
      }

          }

    if (props.coords!==null){
      updateMarker()
    }
    watch(() => props.coords, updateMarker,{ deep: true });
    return [
    ]
  },

}

</script>

<style scoped>

</style>