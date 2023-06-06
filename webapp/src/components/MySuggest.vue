<template>
  <div>
    <div class="inputs row">
      <div class="col-1">
        <div v-if="atMapObjectsIndexes.__v_raw.length>0">
          <button class="fa-btn">
            <i class="fa fa-map-marker" aria-hidden="true" @click="ClickOnlyNeedRoutesButtonEvent"></i>
          </button>
        </div>
      </div>
      <div class="number col-1">
        <div v-if="suggestValue.length>0">
          <h4>{{suggestNumber}}</h4>
        </div>
      </div>
      <div class="input col-8">
        <div class="suggest-input">
          <input placeholder="Адрес" :value="suggestValue" :readonly="isInputDisabled" @blur="changeUpdateInput" @change="changeUpdateInput" @input="updateInput" type="text" ref="refInput" >
        </div>
      </div>
      <div class="input col-2">
        <div class="count-input">
          <input class="px-0"  :value="count" type="number" :min="1" :max="100000" @input="updateCount">
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import {mapState, useStore} from "vuex";
import {watch} from "vue";

export default {
  name: "my-suggest",
  data:()=>{
    return {
    }

  },


  props:{
    suggestNumber:{
      type:Number,
      required:true
    },
    suggestValue:{
      type:String,
      required:true
    },
    count:{
      type:Number,
      required:true
    },
    atMapObjectsIndexes:{
      type:Array,
      required:true,
      deep: true
    },
  },



  methods:{
    updateInput(event){
      this.$emit('updateInputEvent', event.target.value)
    },
    changeUpdateInput(event){
      setTimeout(() => {
        this.updateInput(event)
      }, 200);
    },

    updateCount(event){
      this.$emit('updateCountEvent', event.target.value)

    },

    ClickOnlyNeedRoutesButtonEvent(){
      this.$emit('ClickOnlyNeedRoutesButtonEvent', this.atMapObjectsIndexes.__v_raw)
    },

    initializeSuggestView(){
      new window.ymaps.SuggestView(this.$refs.refInput,{
        options: {
          itemLayout: '<span class="ymaps-suggest-view-item">{{ data.value }}</span>'
        },
      });
    },
  },

  mounted() {
    let store = useStore();
    if (store.state.YAPIModule.connected){
      this.initializeSuggestView(); // Ваш метод initializeMap()
    }
    else {
      watch(
          () => store.state.YAPIModule.connected,
          (newValue) => {
            if (newValue) {
              this.initializeSuggestView(); // Ваш метод initializeMap()
            }
          }
      );
    }
  },
  computed:{
    ...mapState('GlobalSettingModule', ['isInputDisabled']), // Подключите состояние из модуля к вычисляемым свойствам
  }



};
</script>
<style>
:root {
  --input-color-border: #ccd2d3;
}

body{
  color: black;
}
.number{
  padding-top: 1%;
  color: white;
}

.fa-map-marker{
 font-size: 25px;
}
.ymaps-suggest-view-item {
  color: #000000; /* Цвет текста подсказки */
}


.inputs{
  display: flex;

}








.input {
  position: relative;
}

.input input {
  border: 0;
  width: 100%;
  font-size: 15px;
  line-height: 35px;
  height: 30px;
  text-align: center;
  background: transparent;
  color: #d7d9de;
}



.input input:focus {
  outline: 0;
  color: #eae5e5;
}

.input input::placeholder {
  color: #d2d2d2;
}

.suggest-input{
  border-bottom: 2px solid #dddde7;

}
.count-input{
  border: 2px solid #e3e2e2;
  border-radius: 10px;
  min-width: 40px;
  margin-top: -2px;
  margin-left: 5px;
  padding-left: 15px;

}

.suggest-input.serious input {
  letter-spacing: 2px;
  text-transform: uppercase;
  font-family: 'Andada', serif;
  font-weight: 500;
}

.suggest-input.modern input {
  font-family: 'Raleway', sans-serif;
  text-transform: lowercase;
  font-weight: 300;
  letter-spacing: 10px;
}

.suggest-input.cheeky input {
  font-family: 'Permanent Marker', cursive;
  font-size: 40px;
}

@keyframes shaker {
  0% {
    transform: translate(0px, 0px) rotate(0deg);
    opacity: 0.8;
  }
  10% {
    transform: translate(10px, 7px) rotate(-9deg);
    opacity: 0.6;
  }
  20% {
    transform: translate(13px, -19px) rotate(-3deg);
    opacity: 0.3;
  }
  30% {
    transform: translate(-6px, -6px) rotate(2deg);
    opacity: 0.4;
  }
  40% {
    transform: translate(-9px, -18px) rotate(-5deg);
    opacity: 0.4;
  }
  50% {
    transform: translate(10px, -8px) rotate(5deg);
    opacity: 0.7;
  }
  60% {
    transform: translate(-10px, 14px) rotate(-6deg);
    opacity: 1;
  }
  70% {
    transform: translate(10px, 3px) rotate(6deg);
    opacity: 0.1;
  }
  80% {
    transform: translate(-2px, 20px) rotate(-6deg);
    opacity: 1;
  }
  90% {
    transform: translate(-7px, -19px) rotate(2deg);
    opacity: 0.5;
  }
}

</style>