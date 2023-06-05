<template>
<div>
  <h5>Способ доставки</h5>
  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio"  id="typeTransportAuto" name="typeTransport" value="auto" :disabled="isInputDisabled" :checked="typeTransport=='auto'" @change="typeTransportUpdate('auto')">
    <label class="form-check-label" for="typeTransportAuto">
      <i class="fa fa-car" aria-hidden="true"></i>
    </label>
  </div>
  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio"  id="typeTransportBicycle" name="typeTransport" value="bicycle" :disabled="isInputDisabled" :checked="typeTransport=='bicycle'" @change="typeTransportUpdate('bicycle')">
    <label class="form-check-label" for="typeTransportBicycle">
      <i class="fa fa-bicycle" aria-hidden="true"></i>
    </label>
  </div>
  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio"  id="typeTransportPedestrian" name="typeTransport"  value="pedestrian" :disabled="isInputDisabled"  :checked="typeTransport=='pedestrian'" @change="typeTransportUpdate('pedestrian')">
    <label class="form-check-label" for="typeTransportPedestrian">
      <i class="fas fa-walking"></i>
    </label>
  </div>

</div>
</template>

<script>

import {mapState} from "vuex";

export default {
  name: "TypeTransport",
  data(){
    return{
    }
  },
  props:{
    typeTransport:{
      type:String,
      required:true
    },

  },
  methods:{
    typeTransportUpdate(value){
      this.$emit("typeTransportUpdateEvent",value)
    }
  },

  computed:{
    ...mapState({
      isInputDisabled: state => state.GlobalSettingModule.isInputDisabled
    })
  }
}

</script>

<style scoped>

</style>