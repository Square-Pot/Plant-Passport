var current_plant = JSON.parse(document.getElementById('current_plant').textContent);
var csrftoken = Cookies.get('csrftoken');

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
      console.log(new_tag);
      //console.log(current_plant);
      // POST request using axios with error handling
      // axios.post("https://galangal.ru/api/", new_tag)
      //   .then(response => this.articleId = response.data.id)
      //   .catch(error => {
      //   this.errorMessage = error.message;
      //   console.error("There was an error!", error);
      // });

      // const likebutton = (id) => {
      //   axios.post(`/api/post/${id}/like/`, { headers: { 'X-CSRFToken': csrftoken } })
    }


    }
  }
})

  
  
  
  