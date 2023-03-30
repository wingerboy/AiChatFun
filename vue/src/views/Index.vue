<template>
  <div class="index">
    <div class="index_contain">
      <div class="index_contain_left">
        <el-input
          v-model="apiKey"
          placeholder="API KEY输入框"
        ></el-input>
        <div class="index_contain_left_contain">
          <div class="iclc_btn">
            <div
              class="iclc_btn_color"
              :style="'left:'+(paperType?'calc(50% - 9.25px);':'0;')"
            ></div>
            <div
              class="iclc_btn_item"
              :style="paperType==0?'color:#fff':''"
              @click="changePaperType(0)"
            >模型选择</div>
            <div
              class="iclc_btn_item"
              :style="paperType==1?'color:#fff':''"
              @click="changePaperType(1)"
            >prompt</div>
          </div>
          <div v-if="paperType==0">
            <div class="iclc_model">
              <el-radio
                v-model="modelType"
                label="1"
              >model1</el-radio>
              <el-radio
                v-model="modelType"
                label="2"
              >model12</el-radio>
            </div>
            <div style="margin-top:10px">topk:{{topk/100}}</div>

            <el-slider v-model="topk"></el-slider>
            <div style="margin-top:10px">tem:{{tem/100}}</div>
            <el-slider v-model="tem"></el-slider>
          </div>
          <div v-if="paperType==1">
            <textarea class="iclc_textarea"></textarea>
          </div>
          <div class="iclc_file">
            <div class="iclc_file_btn">文件上传</div>
            <el-input
              class="iclc_file_input"
              v-model="link"
              placeholder="论文链接输入框"
            ></el-input>
          </div>
          <div
            class="iclc_submit"
            @click="submit"
          >提交</div>
        </div>
      </div>
      <div class="index_contain_right">{{result}}</div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      //openAi密钥
      apiKey: "",
      //选择论文类型
      paperType: 0,
      //模型类型
      modelType: "1",
      //参数
      prompt: "",
      topk: 30,
      tem: 30,
      //链接
      link: "",
      // 结果
      result: "",
    };
  },
  methods: {
    //修改论文类型
    changePaperType(e) {
      this.paperType = e;
    },
    //提交
    submit() {
      var tmp_form = {
        //openAi密钥
        apiKey: this.apiKey,
        //选择论文类型
        paperType: this.paperType,
        //模型类型
        modelType: this.modelType,
        //参数
        prompt: this.prompt,
        topk: this.topk / 100,
        tem: this.tem / 100,
        //链接
        link: this.link,
      };
      this.axios
        .post("/api/request_paper_summary", tmp_form)
        .then((res) => {
          console.log(res);
          this.result = res.data.data;
        })
        .catch((err) => [console.log(err)]);
    },
  },
  components: {},
  mounted() {},
};
</script>
<style lang="scss">
@import "../scss/Index.scss";
</style>