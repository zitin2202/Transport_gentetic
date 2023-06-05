<template>
  <div v-if="!isEmptyLocalStorage">
    <div class="clear-storage">
      <button @click="RemoveLocalData" class="clear-button">
        <img src="@/assets/clearIcon.png" alt="Отчистка данных" class="clear-icon">
      </button>
    </div>
  </div>
  <div v-if="isInputDisabled">
    <div class="d-flex justify-content-center align-items-center spinner"></div>
  </div>
  <div class="container">
    <yandex-map :key="mainMap.id" :center="[55.751244, 37.618423]" :zoom="12">
      <yandex-markers :markers="filteredMarkers" :mapId="mainMap.id" @updateMarkerObjectEvent="updateMarkerObject"/>
    </yandex-map>
    <div class="block total-div">
      <div class="one-div-in-total justify-content-end row ">
        <div class="col-md-6 text-center my-3">
          <h3 class="suggest-label">Точки отправления</h3>
          <my-suggests :suggests="suggestsStore" @updateInputEvent="updateInput" @updateCountEvent="updateCount" @ClickOnlyNeedRoutesButtonEvent="OnlyNeedRoutesToMap"/>
        </div>
        <div class="col-md-6 text-center  my-3">
          <h3 class="suggest-label">Точки назначения</h3>
          <my-suggests :suggests="suggestsDestination" @updateInputEvent="updateInput" @updateCountEvent="updateCount" @ClickOnlyNeedRoutesButtonEvent="OnlyNeedRoutesToMap"/>
        </div>
      </div>
      <div class="two-div-in-total" v-if="routes.atMapObjects.length>0">
        <button class="fa-btn" @click="AllRoutesToMap">
          <i class="fa fa-map"></i>
        </button>
      </div>
    </div>
    <div class="row my-5 setting block">
      <div class="col-4" >
        <my-capacity :capacity="capacity" @updateCapacityEvent="updateCapacity"></my-capacity>
      </div>
      <div class="col-4 text-center">
        <type-transport :type-transport="typeTransport" @typeTransportUpdateEvent="typeTransportUpdate"/>
      </div>
      <div class="col-4 text-center">
        <type-metrics :type-measurement="typeMeasurement" @typeMeasurementUpdateEvent="typeMeasurementUpdate"/>
      </div>
    </div>
    <div class=" route-calculation text-center my-5">
      <route-calculation :storeCoords="filteredStoreCoords" :destinationCoords="filteredDestinationCoords" :storeCount="storeCount" :destinationCount="destinationCount" :capacity="capacity" :IsMinCoords="IsMinCoords" :typeTransport="typeTransport" :typeMeasurement="typeMeasurement"  @updateRoutesEvent="updateRoutes"></route-calculation>
    </div>
    <div class="total-div" v-if="table.body.length>0">
      <table-result class="one-div-in-total" :table="this.table"/>
      <div class="two-div-in-total">
        <a class="fa-btn" :href="excelLink" download="routes.xlsx">
          <i class="fa fa-file-excel"></i>
        </a>
      </div>
    </div>
    <footer class="footer">
    </footer>
  </div>
</template>

<script>
import {onMounted, watch} from "vue";
import {mapState, useStore} from 'vuex';
import MySuggests from "@/components/MySuggests";
import { v4 as uuidv4 } from 'uuid';
import YandexMarkers from "@/components/YandexMarkers";
import RouteCalculation from "@/components/RouteCalculation";
import MyCapacity from "@/components/MyCapacity";
import TableResult from "@/components/TableResult";
import CircularJSON from 'circular-json';
import TypeTransport from "@/components/TypeTransport";
import TypeMetrics from "@/components/TypeMetrics";
import * as XLSX from 'xlsx'

export default {
  name: 'App',
  components: {TableResult, MyCapacity, RouteCalculation, YandexMarkers, MySuggests,TypeTransport,TypeMetrics},
  data: function(){
    return {
      isComputedLoad : false,
      isMapLoad :false,
      isEmptyLocalStorage : true,
      typeTransport: "auto",
      typeMeasurement:"distances",
      mapCenter: [55.751244, 37.618423], // Координаты центра карты
      mapZoom: 10, // Уровень масштабирования карты
      mainMap: {
        id:uuidv4(),
      },
      capacity: 1,
      suggestsStore:this.defaultSuggest(),
      suggestsDestination:this.defaultSuggest(),
      routes:{
        distribution:[],
        ways:[],
        atMapObjects:[],
        colors: [
          '#ff0000', // Красный
          '#0000ff', // Синий
          '#00ff00', // Зеленый
          '#ffff00', // Желтый
          '#ffa500', // Оранжевый
          '#800080', // Фиолетовый
          '#000000', // Черный
          '#ffffff', // Белый
          '#808080', // Серый
          '#40e0d0', // Бирюзовый
          '#00ffff', // Голубой
          '#ff1493', // Малиновый
          '#a52a2a', // Коричневый
          '#800000', // Бордовый
          '#800080', // Пурпурный
          '#00ff00', // Цвет лайма
          '#ffff00', // Лимонный
          '#ff69b4', // Розовый
          // Дополнительные цвета
          '#8b0000', '#1e90ff', '#006400', '#f08080', '#ff8c00', '#9932cc', '#008080', '#ffa07a', '#7fffd4', '#ff00ff',
          '#f4a460', '#7cfc00', '#da70d6', '#00fa9a', '#dda0dd', '#8fbc8f', '#4682b4', '#d8bfd8', '#32cd32', '#f5f5dc',
          '#000080', '#b0c4de', '#ff4500', '#228b22', '#fa8072', '#90ee90', '#778899', '#ffebcd', '#00ced1', '#d3d3d3',
          '#7b68ee', '#f0e68c', '#4b0082', '#bdb76b', '#2e8b57', '#bc8f8f', '#ff6347', '#6b8e23', '#9370db', '#3cb371',
          '#afeeee', '#191970', '#ff7f50', '#556b2f', '#dda0dd', '#add8e6', '#8b4513', '#8b4513'
        ],
      },
      table:{
        head: [],
        body:[],
      },

    }
  },
  methods:{

    defaultSuggestValue(){
      return {id:uuidv4(),value:"",count:1,atMapObjectsIndexes:[]}
    },

    defaultSuggest(){
      return {
        values:[
          this.defaultSuggestValue(),
        ],
        markers:[
        ]
      }
    },

    updateInput(value,index,suggests){
      suggests.values[index].value = value;
      this.markerCheck(index,suggests)
    },
    updateCount(value,index,suggests){
      value = Number(value)
      suggests.values[index].count = value;
      if (suggests.values[index].count<1){suggests.values[index].count=1}

      if (suggests===this.suggestsStore){
        this.LocalStorageSetItem('values','suggestsStore','suggestsStoreValues')
      }
      else {
        this.LocalStorageSetItem('values','suggestsDestination','suggestsDestinationValues')
      }

    },
    updateMarkerObject(object,index,markers){
      markers[index].object = object;
    },
    updateCapacity(value){
      this.capacity = Number(value);
    },
    typeTransportUpdate(value){
      this.typeTransport = value
    },

    typeMeasurementUpdate(value){
      this.typeMeasurement = value
    },

    markerLoad(index,suggests,coordinates){
      let markers = suggests.markers;
      let suggests_value = suggests.values
      if (markers.length-1<index){
        markers.push({id:uuidv4(), coords:null,object:null,type:(suggests===this.suggestsStore ? "store" : "destination")})
      }
      markers[index].coords = coordinates
      if(suggests_value.length-1 === index){
        suggests_value.push(this.defaultSuggestValue())
      }

    },
    markerCheck(index,suggests){
      let suggests_value = suggests.values;
      let markers = suggests.markers;
      let address = suggests_value[index].value
      console.log(address)
      if (address.length === 0){address=" "}
      window.ymaps.geocode(address).then((response) => {
        const geoObjects  = response.geoObjects;
        if (geoObjects.getLength() > 0) {
          const coordinates = geoObjects.get(0).geometry.getCoordinates();
          this.markerLoad(index,suggests,coordinates)

        }
        else {
          console.log(123)
          markers[index].coords = null;

          setTimeout(()=>{
            if (suggests_value.length>1 && suggests_value[index].value<2 && index !== suggests_value.length-1){
              suggests_value.splice(index,1)
              markers.splice(index,1)
            }

            else if (suggests_value.length>1 && index === suggests_value.length-2 && suggests_value[suggests_value.length-1].value.length < 2){
              suggests_value.splice(suggests_value.length-1,1)
            }

          },100)

        }

      });

      setTimeout(()=>{
        if (suggests===this.suggestsStore){
          this.LocalStorageSetItem('values','suggestsStore','suggestsStoreValues')
          this.LocalStorageSetItem('filteredStoreCoords',null,"storeCoords")
        }
        else {
          this.LocalStorageSetItem('values','suggestsDestination','suggestsDestinationValues')
          this.LocalStorageSetItem('filteredDestinationCoords',null,"destinationCoords")
        }
      },200)

    },

    filteredNewCoords(markers) {
      return markers.map((marker) => marker.coords)
    },

    CountPoint(suggests) {
      return suggests.map((suggest) => suggest.count).slice(0, -1)
    },

    updateRoutes(result){
      console.log(result)
      this.removeRotesAtMap()
      this.routes.distribution = result.distribution
      this.routes.ways = result.ways
      this.updateRoutesAtMap()

      this.tableCreate();
      this.LocalStorageSetItem('table')
    },

    updateRoutesAtMap(){
      for (let i=0; i<this.suggestsStore.values.length;i++) {
        this.suggestsStore.values[i].atMapObjectsIndexes = []
      }

      for (let i=0; i<this.suggestsDestination.values.length;i++) {
        this.suggestsDestination.values[i].atMapObjectsIndexes = []
      }


      this.routes.atMapObjects = []
      let map = this.store.state.MainMapModule.MainMap.__v_raw
      for (var i=0; i<this.routes.distribution.length;i++) {
        for (var j = 0; j < this.routes.distribution[i].length; j++) {

          if (this.routes.distribution[i][j] !== 0) {

            if(this.routes.ways.__v_raw[i][j].length === 0){
              continue
            }
            let points = [this.filteredStoreCoords[i]]
            for (var point_index=0; point_index<this.routes.ways.__v_raw[i][j].length;point_index++){
              points.push(this.filteredDestinationCoords[this.routes.ways.__v_raw[i][j][point_index]])
            }

            var multiRoute = new window.ymaps.multiRouter.MultiRoute({
                  referencePoints: points,
                  params: {
                    //Тип маршрутизации - пешеходная маршрутизация.
                    routingMode: this.typeTransport
                  }
                },
                {
                  routeActiveStrokeColor: this.routes.colors[this.routes.atMapObjects.length], // Установка цвета линии маршрута
                  boundsAutoApply: true,
                  wayPointDraggable:false,
                  viaPointDraggable:false,
                  avoidTrafficJams: false,

                },
            );
            map.geoObjects.add(multiRoute)
            this.routes.atMapObjects.push(multiRoute)
            let objectIndex = this.routes.atMapObjects.length-1
            this.suggestsStore.values[i].atMapObjectsIndexes.push(objectIndex)
            for (var p_index=0; p_index<this.routes.ways.__v_raw[i][j].length;p_index++){
              this.suggestsDestination.values[this.routes.ways.__v_raw[i][j][p_index]].atMapObjectsIndexes.push(objectIndex)
            }
          }
        }
      }
    },

    OnlyNeedRoutesToMap(atMapObjectsIndexes) {
      this.removeRotesAtMap()

      let map = this.store.state.MainMapModule.MainMap.__v_raw
      let needObjects = atMapObjectsIndexes.map(index => this.routes.atMapObjects[index].__v_raw)
      console.log(needObjects)
      for (var i = 0; i < needObjects.length; i++) {
        map.geoObjects.add(needObjects[i])
      }
    },

    AllRoutesToMap() {
      this.removeRotesAtMap()
      let map = this.store.state.MainMapModule.MainMap.__v_raw
      for (var i = 0; i < this.routes.atMapObjects.length; i++) {
        map.geoObjects.add(this.routes.atMapObjects[i].__v_raw)
      }
    },

    removeRotesAtMap(){
      let map = this.store.state.MainMapModule.MainMap.__v_raw
      for (var i=0; i<this.routes.atMapObjects.length;i++){
        let routeObj = this.routes.atMapObjects[i].__v_raw
        map.geoObjects.remove(routeObj)

      }

    },

    tableCreate(){
      this.table.head = []
      this.table.head.push("Адрес поставщика")
      let maxLenght = 0
      this.table.body = [];
      this.table.maxLineLength = 0
      for (var i=0; i<this.routes.ways.length;i++){
        for (var j=0; j<this.routes.ways[i].length;j++){
          if (this.routes.ways[i][j].length>0){
            let line = [];
            line.push(this.suggestsStore.values[i].value);
            let lineLength = 0;
            for (var chain_index=0; chain_index<this.routes.ways[i][j].length;chain_index++){
              let destination_index = this.routes.ways[i][j][chain_index];
              line.push(this.suggestsDestination.values[destination_index].value + " (" + this.routes.distribution[i][destination_index] + ")");
              lineLength+=1;
            }
            this.table.body.push(line);
            if (lineLength>maxLenght){
              maxLenght=lineLength
            }

          }

        }
      }

      for (var n=0;n<maxLenght;n++){
        this.table.head.push("Поставка " + (n+1))

      }
    },

    LocalStorageGetItem(nameValue,objName=null,localName=nameValue,Return=false){
      const localItem = JSON.parse(localStorage.getItem(localName));
      if (localItem !== undefined && localItem !== null) {
        if (Return){
          return localItem
        }
        else if (objName!==null){
          this[objName][nameValue]=localItem;
        }
        else {
          this[nameValue]=localItem;
        }
      }
      else {
        return false
      }





    },

    LocalStorageSetItem(nameValue,objName=null,localName=nameValue){
      this.isEmptyLocalStorage = false
      let serializedData = null;
      if (objName!==null){
        serializedData = CircularJSON.stringify(this[objName][nameValue]);
      }
      else {
        serializedData = CircularJSON.stringify(this[nameValue]);
      }
      localStorage.setItem(localName,serializedData);

    },

    MarkersLocalLoad(suggests,coords){
      if (coords){
        for (var i=0;i<coords.length;i++){
          // console.log(i)
          // console.log(suggests)
          // console.log(coords[i])
          // console.log('________________')

          if (coords[i]!==null){
            this.markerLoad(i,suggests,coords[i])

          }

        }
      }


    },

    LocalAllLoad(){
      this.LocalStorageGetItem("values","suggestsStore","suggestsStoreValues");
      this.LocalStorageGetItem("values","suggestsDestination","suggestsDestinationValues");
      this.LocalStorageGetItem("capacity");
      this.LocalStorageGetItem("typeTransport");
      this.LocalStorageGetItem("typeMeasurement");
      this.LocalStorageGetItem("distribution","routes");
      this.LocalStorageGetItem("ways","routes");

      this.LocalStorageGetItem("table");

      let storeCoords = this.LocalStorageGetItem("storeCoords",null,"storeCoords",true)
      let destinationCoords = this.LocalStorageGetItem("destinationCoords",null,"destinationCoords",true)

      if (storeCoords || destinationCoords){
        this.WhenMapLoad(()=>{
            this.MarkersLocalLoad(this.suggestsStore,storeCoords)
            this.MarkersLocalLoad(this.suggestsDestination,destinationCoords)
          })
      }

      if (this.filteredStoreCoords.length>0 && this.filteredDestinationCoords.length>0){
        this.WhenMapLoad(this.updateRoutesAtMap)
        this.isComputedLoad = true
        console.log("YESSSS")
      }
      else {
        watch(
            () => this.filteredStoreCoords,
            (newValue) => {
              if (newValue.length>0 && this.isComputedLoad===false) {
                this.WhenMapLoad(this.updateRoutesAtMap)
                this.isComputedLoad = true
                console.log("YESSSS")
              }
            },
        );

      }



    },

    RemoveLocalData(){
      localStorage.clear();
      this.isEmptyLocalStorage = true
      this.capacity = 1;
      this.typeTransport = "auto";
      this.typeMeasurement = "distances";
      this.suggestsStore = this.defaultSuggest();
      this.suggestsDestination = this.defaultSuggest();
      this.routes.ways = [];
      this.routes.distribution = [];
      this.routes.atMapObjects = [];
      this.table ={body:[], head: []};

      let map = this.$store.state.MainMapModule.MainMap.__v_raw
      console.log(map)
      map.geoObjects.removeAll();


    },

    WhenMapLoad(functionBody){
      if ( this.store.state.MainMapModule.MainMap!=null){
        functionBody()
        this.isMapLoad = true;
      }
      else {
        watch(
            () => this.store.state.MainMapModule.MainMap,
            (newValue) => {
              if (newValue!==null && this.isMapLoad === false) {
                functionBody()
                this.isMapLoad = true;
              }
            },

        );

      }
    }

  },




  setup(){
    let store = useStore();
    const CheckConnectAPI = () => {
      store.dispatch('YAPIModule/CheckConnectAPI');
    };
    onMounted(() => {
      CheckConnectAPI();
    });

    return{
      store
    }
  },

  mounted() {
    if (localStorage.length!==0){
      this.isEmptyLocalStorage = false
      this.LocalAllLoad()

    }
  },

  computed: {
    filteredMarkers() {
      return this.suggestsStore.markers
          .concat(this.suggestsDestination.markers);
    },

    filteredStoreCoords() {
      return this.filteredNewCoords(this.suggestsStore.markers)
    },
    filteredDestinationCoords() {
      return this.filteredNewCoords(this.suggestsDestination.markers)
    },

    StoreCoordsNOTNULL() {
      return this.filteredStoreCoords.filter(coords=>coords!==null)
    },
    DestinationCoordsNOTNULL() {
      return this.filteredDestinationCoords.filter(coords=>coords!==null)
    },
    storeCount() {
      return this.CountPoint(this.suggestsStore.values)
    },
    destinationCount() {
      return this.CountPoint(this.suggestsDestination.values)
    },

    IsMinCoords() {
      return this.StoreCoordsNOTNULL.length>1 && this.DestinationCoordsNOTNULL.length>1
    },

    ...mapState('GlobalSettingModule', ['isInputDisabled']), // Подключите состояние из модуля к вычисляемым свойствам


    excelLink() {
      if (this.table.head.length>0){
        // Создание пустой книги
        const workbook = XLSX.utils.book_new();
        // Создание листа
        let value = []
        value.push(this.table.head);
        value = value.concat(this.table.body)
        const worksheet = XLSX.utils.aoa_to_sheet(value);
        // Добавление листа в книгу
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Лист 1');
        // Преобразование книги в бинарный формат
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        // Создание Blob из бинарных данных
        const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

        // Создание ссылки на скачивание файла
        const url = URL.createObjectURL(blob);
        return url;

      }

      return '';
    }


  },
  watch:{
    capacity(){
      if (this.capacity!==1){
        this.LocalStorageSetItem('capacity')
      }
    },
    typeTransport(){
      if (this.typeTransport!=='auto'){
        this.LocalStorageSetItem('typeTransport')
      }
    },
    typeMeasurement(){
      if (this.typeMeasurement!=='distances'){
        this.LocalStorageSetItem('typeMeasurement')
      }
    },
    'routes.ways'(){
      if (this.routes.ways.length === 0 && this.routes.distribution.length === 0){
        localStorage.removeItem("ways");
        localStorage.removeItem("distribution");
      }
      else {
        this.LocalStorageSetItem('ways','routes')
        this.LocalStorageSetItem('distribution','routes')
      }
    },
  }


}
</script>
<style>

@font-face {
  font-family: 'CustomFont';
  src: url('@/assets/fonts/ofont.ru_Montserrat Alternates.ttf') format('woff2');
  /* Другие форматы шрифта, если они есть */
}

body {
  font-family: 'CustomFont', sans-serif;
}

body{
  padding: 10px;
  background: url("@/assets/black001.jpg");

}

.block{
  border-radius: 15px;
  background: #343134;

}

.setting{
  padding: 1%;
  color: white;


}



.suggest-label{
  margin-bottom: 5%;
  color: white;

}


.clear-storage{
  top:0;
  left: 0;
  position: fixed;
  z-index: 45;
  width: 4%;
  min-width: 70px;
  padding-bottom: 100%
}



.clear-button{
  height: 100%;
  width: 100%;
  background: white;
  border-radius: 5px;
}

.clear-button:hover{
  background: #f5f5f5;
}

.clear-icon{
  height: 100%;
  width: 100%;
}

.route-calculation{
  height: 100%;
  width: 100%;
}

.form-check i{
  font-size: 30px;
}
.form-check input{
  font-size: 20px;
}

.total-div{
  display: flex;
  align-items: flex-start; /* Выравнивание по верхней границе */
  margin-top: 6%;

}

.one-div-in-total{
  width: 100%;
  flex-shrink: 0; /* Запрет сжатия объекта */
  margin-right: 4%;
  font-size: 20px;
}
.two-div-in-total{
  line-height: 1;
  font-size: 55px;
}
.fa-btn{
  color: white;
  background-color: transparent;
  border: none;
}

.fa-btn:hover{
  color: #e1e1e1;
}


.spinner {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  border: 6px solid #000000;
  border-top: 6px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
