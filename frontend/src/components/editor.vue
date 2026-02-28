<template>
   <quill-editor 
      v-model:content="content"
      :options="editorOption"
      contentType="html"
      theme="snow"
      @ready="onEditorReady"
   ></quill-editor>
</template>

<script>
import {QuillEditor} from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import api from '../api';

export default {
  components: {QuillEditor},
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  data() {
      return {
         content: this.modelValue,
         editorOption: {
            modules: {
               toolbar: [
                 ['bold', 'italic', 'underline', 'strike'],
                 ['blockquote', 'code-block'],
                 [{ 'header': 1 }, { 'header': 2 }],
                 [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                 [{ 'script': 'sub' }, { 'script': 'super' }],
                 [{ 'indent': '-1' }, { 'indent': '+1' }],
                 [{ 'direction': 'rtl' }],
                 [{ 'size': ['small', false, 'large', 'huge'] }],
                 [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                 [{ 'color': [] }, { 'background': [] }],
                 [{ 'font': [] }],
                 [{ 'align': [] }],
                 ['clean'],
                 ['link', 'image']
               ]
           }
        },
        quill: null
     }
  },
  methods: {
    onEditorReady(quill) {
      this.quill = quill;
      // 重写图片处理函数
      const toolbar = quill.getModule('toolbar');
      toolbar.addHandler('image', this.handleImageUpload);
    },
    handleImageUpload() {
      const input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.setAttribute('accept', 'image/*');
      input.click();
      
      input.onchange = async () => {
        const file = input.files[0];
        if (file) {
          try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await api.post('/upload/image', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });
            
            if (response.data.url) {
              const range = this.quill.getSelection();
              this.quill.insertEmbed(range.index, 'image', response.data.url);
              this.quill.setSelection(range.index + 1);
            }
          } catch (error) {
            console.error('上传图片失败:', error);
          }
        }
      };
    }
  },
  watch: {
    modelValue(newVal) {
      this.content = newVal;
    },
    content(newVal) {
      this.$emit('update:modelValue', newVal);
    }
  }
}
</script>
