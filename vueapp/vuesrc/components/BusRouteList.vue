<template>
  <div class="container-fluid">
    <table class="table table-sm table-striped">
      <thead>
        <tr>
          <th>Route</th>
          <th>Bus</th>
          <th>Name</th>
          <th>Teacher</th>
          <th>Attendant</th>
          <th>Driver</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(obj, idx) in object_list" :key="idx">
          <td><a :href="'/transport/routes/' + obj.id + '/'">
            {{ obj.route }}
          </a></td>
          <td>{{ obj.registration }}</td>
          <td>{{ obj.name }}</td>
          <td>{{ obj.teacher }}</td>
          <td>{{ obj.attendant }}</td>
          <td>{{ obj.driver }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      object_list: null,
    };
  },
  mounted() {
    this.object_list = JSON.parse(document.getElementById("data").text);
    this.object_list.forEach(el => {
      console.log("el =", el);
    });
  }
}
</script>

<style>

</style>