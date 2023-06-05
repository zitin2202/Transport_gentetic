<template>
  <div class="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" :key="marker.id" v-for="(marker,index) in markers">
    <yandex-marker :marker-number="(marker.type==='store' ? index+1 : index+1 - markersStoreCount)" :coords="marker.coords" :object="marker.object" :type="marker.type" @updateMarkerObjectEvent="updateMarkerObject($event,index)"/>
  </div>
</template>

<script>
import YandexMarker from "@/components/YandexMarker";

export default {
  name: "yandex-markers",
  components: {YandexMarker},

  props: {
    markers: {
      type: Array,
      required: true
    },
  },

  methods: {
    updateMarkerObject(object, index) {
      console.log('emiiit')
      this.$emit('updateMarkerObjectEvent', object, index, this.markers)

    },
  },
  setup() {
    console.log('markers')
  },

  computed: {
    markersStoreCount() {
      return this.markers.filter((marker) => marker.type === 'store').length
    }
  }
}
</script>

<style scoped>

</style>