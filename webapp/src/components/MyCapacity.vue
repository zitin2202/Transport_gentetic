<template>
  <div class="input text-center">
    <h5>Вместительность транспорта</h5>
    <div class="count-input col-4 mx-auto">
      <input :value="capacity" type="number" min="0" max="1111111" @blur="capacityInput" @change="capacityInput" @input="capacityInput" class="capacityInput">
    </div>
  </div>

 </template>
<script>
export default {
  name: "my-capacity",
  props:{
    capacity:{
      type:Number,
      required:true
    },
  },
  methods:{
    capacityInput(event){
      this.$emit('updateCapacityEvent', event.target.value)
    },
  }
}
</script>

<style scoped>
.capacityInput{
font-size: 20px;
}

</style>