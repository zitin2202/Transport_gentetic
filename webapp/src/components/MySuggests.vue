<template>
  <div>
    <my-suggest class="mx-3" v-for="(suggest, index) in suggests.values" :key="suggest.id" :suggest-number="index+1" :suggest-value="suggest.value" :count="suggest.count" :atMapObjectsIndexes="suggest.atMapObjectsIndexes" @updateInputEvent="updateInput($event, index)" @updateCountEvent="updateCount($event, index)" @ClickOnlyNeedRoutesButtonEvent="ClickOnlyNeedRoutesButtonEvent"></my-suggest>
  </div>
</template>

<script>

import MySuggest from "@/components/MySuggest";

export default {
  name: "my-suggests",
  components: {MySuggest},
  data(){
    return {
    }
  },
  props:{
    suggests:{
      type:Object,
      required:true
    },
  },
  methods: {
    updateInput(newValue,index) {
      const extraProp = this.suggests; // Значение пропса suggests
      this.$emit('updateInputEvent',newValue,index,extraProp)
    },

    updateCount(newValue,index) {
      const extraProp = this.suggests; // Значение пропса suggests
      this.$emit('updateCountEvent',newValue,index,extraProp)
    },

    ClickOnlyNeedRoutesButtonEvent(event){
      this.$emit('ClickOnlyNeedRoutesButtonEvent',event)
    },
  }
}
</script>

<style scoped>

</style>