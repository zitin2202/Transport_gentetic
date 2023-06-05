<template>
<div>
  <table class="table table-dark table-responsive table-striped table-bordered table-hover">
    <thead class="text-center bg-dark ">
      <th v-for="headValue in table.head" :key="headValue">{{headValue}}</th>
    </thead>
    <tbody>
      <tr v-for="(line,index) in table.body" :key="index">
        <td v-for="(cell,index_ceil) in line" :key="'index_ceil'+index_ceil">
          {{cell}}
        </td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script>
export default {
  name: "table-result",
  props:{
    table:{
      type:Object,
      required:true
    },

  }
}
</script>

<style scoped>
.table{
  border: 1px solid #000000;
  flex-shrink: 0; /* Запрет сжатия объекта */

}


</style>