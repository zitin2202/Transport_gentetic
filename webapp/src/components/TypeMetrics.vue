<template>
  <div>
    <h5>Способ измерения</h5>
    <div class="form-check form-check-inline">
      <input class="form-check-input" type="radio"  id="typeMetricsDistance" name="typeMetrics" value="distances" :disabled="isInputDisabled" :checked="typeMeasurement=='distances'" @change="typeMeasurementUpdate('distances')">
      <label class="form-check-label" for="typeMetricsDistance">
        <i class="fa fa-road" aria-hidden="true"></i>
      </label>
    </div>
    <div class="form-check form-check-inline">
      <input class="form-check-input" type="radio"  id="typeMetricsDuration" name="typeMetrics" value="durations" :disabled="isInputDisabled" :checked="typeMeasurement=='durations'" @change="typeMeasurementUpdate('durations')">
      <label class="form-check-label" for="typeMetricsDuration">
        <i class="fa fa-clock"></i>
      </label>
    </div>

  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "metrics-change",
  props:{
    typeMeasurement:{
      type:String,
      required:true
    },
  },
  methods:{
    typeMeasurementUpdate(value){
      this.$emit("typeMeasurementUpdateEvent",value)
    }
  },
  computed: {
    ...mapState({
      isInputDisabled: state => state.GlobalSettingModule.isInputDisabled
    }),

  }
}
</script>

<style scoped>

</style>