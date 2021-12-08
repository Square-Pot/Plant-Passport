/* Get vars from template  */
var current_plant_is_seed = current_plant.is_seed;


/* Vue.js */

// app
var app_seeds = new Vue({
  el: "#is_seed",
  data: {
    is_seeds: false,
    disabled: false,
  },
  methods: {
    check: async function(e) {
      console.log(this.is_seeds);
      this.disabled = true;
      if (this.is_seeds){
        const set_is_seed_url = `${api_url}/set_as_seed/${current_plant.id}`;
        console.log(set_is_seed_url);
        await axios.get(set_is_seed_url).then((resp) => {
          console.log(resp.data);
        });
      }else {
        const set_is_seed_url = `${api_url}/unset_as_seed/${current_plant.id}`;
        console.log(set_is_seed_url);
        await axios.get(set_is_seed_url).then((resp) => {
          console.log(resp.data);
        });
      }
      this.disabled = false;
  },
    get_seed_status: function(){
      console.log('Init seed status');
      console.log(current_plant_is_seed);
      this.is_seeds = current_plant_is_seed;
    },
  },
  created() {
    this.get_seed_status();
  }
});
  
  
  
  