<template>
   <quill-editor 
      v-model:content="content"
      :editorOption="editorOption"
      contentType="html"
      theme="snow"
   ></quill-editor>
</template>

<script>
import {QuillEditor} from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

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
                    // 加粗 斜体 下划线 删除线 -----['bold', 'italic', 'underline', 'strike']
                       ['bold', 'italic', 'underline', 'strike'],
                        // 引用  代码块-----['blockquote', 'code-block']
                       ['blockquote', 'code-block'],
                        // 1、2 级标题-----[{ header: 1 }, { header: 2 }]
                       [{ header: 1 }, { header: 2 }],
                        // 有序、无序列表-----[{ list: 'ordered' }, { list: 'bullet' }]
                       [{ list: 'ordered' }, { list: 'bullet' }],
                        // 上标/下标-----[{ script: 'sub' }, { script: 'super' }]
                       [{ script: 'sub' }, { script: 'super' }],
                        // 缩进-----[{ indent: '-1' }, { indent: '+1' }]
                       [{ indent: '-1' }, { indent: '+1' }],
                        // 文本方向-----[{'direction': 'rtl'}]
                       [{ direction: 'rtl' }],
                        // 字体大小-----[{ size: ['small', false, 'large', 'huge'] }]
                       [{ size: ['small', false, 'large', 'huge'] }],
                        // 标题-----[{ header: [1, 2, 3, 4, 5, 6, false] }]
                       [{ header: [1, 2, 3, 4, 5, 6, false] }],
                        // 字体颜色、字体背景颜色-----[{ color: [] }, { background: [] }]
                       [{ color: [] }, { background: [] }],
                        // 字体种类-----[{ font: [] }]
                       [{ font: [] }],
                        // 对齐方式-----[{ align: [] }]
                       [{ align: [] }],
                        // 清除文本格式-----['clean']
                       ['clean'],
                        // 链接、图片、视频-----['link', 'image', 'video']
                       ['image']
              ]
           }
        }
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
