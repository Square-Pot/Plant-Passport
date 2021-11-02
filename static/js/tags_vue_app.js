var current_plant = JSON.parse(document.getElementById('current_plant').textContent);
//var csrftoken = Cookies.get('csrftoken');

Vue.component('tag-item', {
    props: ['tag'],
    template: '<button type="button" class="btn btn-primary btn-sm mx-2"> \
    {{ tag.text }} <span class="badge bg-secondary">{{ tag.number }}</span> \
  </button>'
  })
  
var app = new Vue({
  el: '#tags',
  data: {
    create_new_shown: false,
    extisitng_tags: [
      { id: 0, text: 'Vegetables', number: 3 },
      { id: 1, text: 'Cheese', number: 23 },
      { id: 2, text: 'Whatever', number: 41 }
    ],
  }, 
  methods: {
    showCreateNewDiv: function () {
      this.create_new_shown = true
    },
    createTagPost: function () {
      const new_tag = { tag_name: this.new_tag, plant_id: current_plant.id};
      const url = `https://8000-tan-sturgeon-gacaq6nm.ws-eu17.gitpod.io/api/add_tag_to_plant/${current_plant.id}/${this.new_tag}`;
      console.log(new_tag);
      console.log(current_plant);
      console.log('url:', url);
      axios.get(url)
        .then((response) => {
        console.log(response.data);
        console.log(response.status);
        console.log(response.statusText);
        console.log(response.headers);
        console.log(response.config);
      });
      // const likebutton = (id) => {
      //   axios.post(`/api/post/${id}/like/`, { headers: { 'X-CSRFToken': csrftoken } })
    }
  }
})

  
  
  
  