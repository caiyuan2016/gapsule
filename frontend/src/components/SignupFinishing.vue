<template>
  <div id="userinfo">

    <h4 style="text-align: center; padding: 10px 0">Fill in your information</h4>

    <b-form @submit="onSubmit">
      <ul class="main">
        <li class="icon">
          <label for="icon">Choose an image as your icon</label>
          <img :src="icon" alt="User Icon" id="icon">
          <input
            id="choose" 
            type="file" 
            name="icon" 
            accept="image/*" 
            @change="changeImg($event)" 
            ref="icon"
          >
        </li>

        <li class="name">
          <b-form-group class="fullname" label="Name" label-for="firstname" horizontal>
            <b-row>
            <b-col cols="6">
              <b-form-input
                id="firstname"
                type="text"
                v-model="firstname"
                placeholder="firstname"
                required
              />
              
            </b-col>
            <b-col cols="6">
              <b-form-input
                id="secondname"
                type="text"
                v-model="secondname"
                placeholder="secondname"
                required
              />
            </b-col>
            </b-row>
          </b-form-group>
        </li>

        <li class="biography">
          <label for="biography">Biography</label>
          <b-form-input 
            id="biography"
            type="text"
            v-model="biography"
          />
        </li>

        <li class="company">
          <label for="company">Company</label>
          <b-form-input
            id="company"
            type="text"
            v-model="company"
          />
        </li>

        <li class="location">
          <label for="location">Location</label>
          <b-form-input
            id="location"
            type="text"
            v-model="location"
          />
        </li>

        <li class="website">
          <label for="website">Website</label>
          <b-form-input
            id="website"
            type="text"
            v-model="website"
          />
        </li>

        <li class="operation">
          <b-button type="submit" variant="primary" class="submit">Submit</b-button>
        </li>
      </ul>
    </b-form>
  </div>
</template>

<script>
// window.onload = function() {
//   let img = document.getElementById('icon');
//   let input = document.getElementById('choose');
//   img.onclick = function() {
//     input.click();
//   }
// }
import axios from 'axios';
export default {
  name: 'SignupFinishing',
  data() {
    return {
      icon: require('../images/choose_icon.jpg'),
      firstname: '',
      secondname: '',
      biography: '',
      company: '',
      location: '',
      website: ''
    }
  },
  methods: {
    changeImg(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      let that = this;
      reader.readAsDataURL(file);
      reader.onload = function() {
        that.icon = this.result;
        // console.log(that.icon);
      } 
    },
    onSubmit(e) {
      e.preventDefault();
      axios({
        method: 'POST',
        url: '/signup/verify/finishing',
        data: {
          ajax: 1,
          icon: this.icon,
          firstname: this.firstname,
          secondname: this.secondname,
          biography: this.biography,
          company: this.company,
          location: this.location,
          website: this.website
        }
      }).then(response => {
        if(response.data.state == 'ok') {
          this.$router.replace('/index');
        }else {
          console.log(response.data.error);
        }
      }).catch(error => {
        console.log(error);
      })
    }
  }
}
</script>

<style scoped>
#userinfo {
  width: 640px;
  height: 100%;
  margin: 0 auto;
}
ul {
  list-style: none;
  margin-top: 1rem;
  border: 1px solid #D7DEE2;
}
ul li {
  list-style: none;
  width: 100%;
  margin-left: -20px;
  padding: 0.6rem 0;
}
.icon > img {
  display: block;
  width: 100px;
  height: 100px;
  background-size: 100%;
}
/* .icon > input {
  display: none;
} */
</style>

<style>
#userinfo .name .fullname label:after{
  content: " *";
  color:red;
}
</style>
