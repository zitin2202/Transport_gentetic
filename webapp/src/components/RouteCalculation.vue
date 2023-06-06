<template>
<button class="btn btn-primary route-calculation-button" @click="SubmitCoords" :disabled="isButtonDisabled">Расчитать маршруты</button>
</template>

<script>
import {mapState, useStore} from "vuex";
import Openrouteservice from 'openrouteservice-js';

export default {
  name: "route-calculation",
  props:{
    storeCoords:{
      type:Array,
      required:true
    },
    destinationCoords:{
      type:Array,
      required:true
    },
    storeCount:{
      type:Array,
      required:true
    },
    destinationCount:{
      type:Array,
      required:true
    },
    capacity:{
      type:Number,
      required:true
    },
    IsMinCoords:{
      type:Boolean,
      required:true
    },
    typeTransport:{
      type:String,
      required:true
    },
    typeMeasurement:{
      type:String,
      required:true
    }

  },
  setup(){
    const store = useStore();
    const orsMatrix = new Openrouteservice.Matrix({ api_key: "5b3ce3597851110001cf624817bc7afc92314896893a12f1234acd86" });

    return {
      store,
      orsMatrix
    }
  },
  methods:{
    GiveResult(result){
      this.$emit('updateRoutesEvent',result)
    },
    ErrorResult(){
      this.$emit('ErrorResultEvent')
    },
    SubmitCoords(){
      this.DistanceCalculationRoutesByOpenRouteAPI()
      .then(response => {

        if (response.metrics.flat().indexOf(null)>-1){
          this.ErrorResult()
          return
        }
        let storeLen = response.storeLen
        let distances = response.metrics.slice(0,storeLen)
        let distanceBetweenDestinations = response.metrics.slice(storeLen)
        let request = {distances:distances,storeCount:this.storeCount,destinationCount:this.destinationCount,capacity:this.capacity,distanceBetweenDestinations:distanceBetweenDestinations}
        this.$store.commit('GlobalSettingModule/setIsInputDisabled',true)
        fetch('http://127.0.0.1:5000/build', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(request)
        })

      .then(response => response.json())
        .then(result => {
          // Обработка ответа от сервера Flask
          this.GiveResult(result)
          this.$store.commit('GlobalSettingModule/setIsInputDisabled',false)
        })
        .catch(error => {
          // Обработка ошибок
          this.$store.commit('GlobalSettingModule/setIsInputDisabled',false)

          console.error('Ошибка:', error);
        });
      })
      .catch(error => {
        console.error(error);
      });

    },


    DistanceCalculationRoutesByOpenRouteAPI(){
          let storeLen = this.storeNotNULL.length //значения нужно добавить в отдельные переменные, так как после окончания обработки промиса, сами переменные могут успеть поменяться
          let destinationLen = this.storeNotNULL.length
          let typeMeasurement = this.typeMeasurement
         return new Promise((resolve, reject) => {
          this.orsMatrix.calculate({
          locations:  this.locations.concat(this.destinationsNotNULL),//добовляю к локациям пукты назначения ещё раз.
          sources: this.storeIndexes.concat(this.destinationsAsStoreIndexes),//обозначаю дублированные пункты назначения, как поставщиков, чтобы узнать расстояние между пунктами назначениями
          destinations: this.destinationsIndexes,
          profile: this.TypeTransportOpenRouteService, // Профиль маршрута
          metrics: ['distance', 'duration'], // Метрики, которые вы хотите получить
        })
        .then(response => {
          resolve({metrics:response[typeMeasurement],storeLen:storeLen,destinationLen:destinationLen})
        })
        .catch(error => {
          reject(error)
        });
      });


    },



  },
  computed:{
    locations(){
      return this.storeNotNULL.concat(this.destinationsNotNULL)
    },
    storeIndexes(){
      return Array.from({ length: this.storeNotNULL.length }, (_, index) => index)
    },
    destinationsIndexes(){
      return Array.from({ length: this.destinationsNotNULL.length}, (_, index) => this.storeNotNULL.length+index)
    },

    destinationsAsStoreIndexes(){
      return Array.from({ length: this.destinationsNotNULL.length}, (_, index) => this.storeNotNULL.length+this.destinationsNotNULL.length+index)
    }

    ,
    storeNotNULL(){
      return this.storeCoords.filter(coords=>coords!==null).map(coords =>[coords[1],coords[0]])
    },
    destinationsNotNULL(){
      return this.destinationCoords.filter(coords=>coords!==null).map(coords =>[coords[1],coords[0]])
    },
    isButtonDisabled(){
      return !this.IsMinCoords || this.isInputDisabled
    },
    TypeTransportOpenRouteService(){
      switch (this.typeTransport){
        case 'auto':
          return "driving-car"
        case 'bicycle':
          return "cycling-regular"
        case 'pedestrian':
          return "foot-walking"
      }
      return null
    },

    ...mapState('GlobalSettingModule', ['isInputDisabled']), // Подключите состояние из модуля к вычисляемым свойствам


  },



}
</script>

<style scoped>
.route-calculation-button{
font-size: 30px;
border-radius: 30px;
padding: 10px;
}
</style>