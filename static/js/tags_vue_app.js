

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
    new_tags: [],

  }, 
  methods: {
    showCreateNewDiv: function () {
      this.create_new_shown = true
    },
    createTagPost: function () {
      console.log('new_tags:', new_tags);
      // POST request using axios with error handling
      const new_tag = { tag_name: new_tag };
      axios.post("https://galangal.ru/api/", new_tag)
        .then(response => this.articleId = response.data.id)
        .catch(error => {
        this.errorMessage = error.message;
        console.error("There was an error!", error);
      });
    }
  }
})

  
  
  
  