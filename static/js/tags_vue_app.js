/* Get vars from template  */
var current_plant = JSON.parse(document.getElementById('current_plant').textContent);
var current_user = JSON.parse(document.getElementById('current_user').textContent);
var api_url = 'https://galangal.ru/api';
//var api_url = 'https://8000-magenta-pike-w7rmbicg.ws-eu17.gitpod.io/api';


/* Get from cookies  */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');


/* Vue.js */

// active tags for current plant
Vue.component("tag-item-active", {
  props: ["tag"],
  template:
    '<button type="button" class="btn btn-primary btn-sm mx-2"  @click="remove_tag(tag.id)">{{ tag.name }}</button>',
  methods: {
    remove_tag(tag_id) {
      this.$emit("remove_tag", tag_id);
    }
  }
});


// other available tags of this user
Vue.component("tag-item-passive", {
  props: ["tag"],
  template:
    '<button type="button" class="btn btn-secondary btn-sm mx-2" @click="add_tag(tag.id)">{{ tag.name }}</button>',
  methods: {
    add_tag(tag_id) {
      this.$emit("add_tag", tag_id);
    }
  }
});

// new tag
Vue.component("cur-plant", {
  props: ["new_tag"],
});


// app
var app = new Vue({
  el: "#tags",
  data: {
    create_new_shown: false,
    active_tags: [],
    passive_tags: [],
    all_tags: [], 
    new_tag: '',
  },
  methods: {
    createTag: function () {
      const new_tag = {
        tag_name: this.new_tag,
        plant_id: current_plant.id,
      };
      axios
        .post(`${api_url}/create_new_tag`, new_tag, {headers: {'X-CSRFToken': csrftoken}})
        .then((response) => {
            console.log(response.data);
        });
    },
    getTags: function () {
      axios
        .get(`${api_url}/get_plant_tags_and_rest/${current_plant.id}/${current_user.id}`)
        .then((response) => {
          this.all_tags = response.data;
          console.log(this.all_tags);
          this.all_tags.forEach(this.sortTags);
        });
    },
    sortTags: function (tag) {
      if (tag.belongs) {
        this.active_tags.push(tag);
      } else {
        this.passive_tags.push(tag);
      }
    },
    removeTag: function (tag_id) {
      const remove_tag_url = `${api_url}/remove_tag_from_plant/${current_plant.id}/${tag_id}`;
      console.log(remove_tag_url);
      axios.get(remove_tag_url).then((response) => {
        console.log(response.data);
        this.active_tags = []
        this.passive_tags = []
        this.getTags()
      });
    },
    addTag: function (tag_id) {
      const add_tag_url = `${api_url}/add_tag_to_plant/${current_plant.id}/${tag_id}`;
      console.log(add_tag_url);
      axios.get(add_tag_url).then((response) => {
        console.log(response.data);
        this.active_tags = []
        this.passive_tags = []
        this.getTags()
      });
    }
  },
  created() {
    this.getTags();
  }
});
  
  
  
  