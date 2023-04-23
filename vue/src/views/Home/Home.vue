<template>
	<div v-loading="loading" class="index">
		<div class="index-contain">
			<div class="index-contain-left">
				<el-input class="index-contain-left-title" v-model="apiKey" placeholder="API KEY输入框"></el-input>
				<el-tabs v-model="activeName" @tab-click="handleClick">
					<el-tab-pane label="模型选择" name="model">
						<div class="index-contain-left-content">
							<div class="iclc-card">
								<el-radio v-model="modelType" label="1">model1</el-radio>
								<el-radio v-model="modelType" label="2">model2</el-radio>
							</div>
							<div class="iclc-card">
								<p>top_p:{{ top_p / 100 }}</p>
								<el-slider v-model="top_p"></el-slider>
								<p>temperature:{{ temperature / 100 }}</p>
								<el-slider v-model="temperature"></el-slider>
							</div>
						</div>
					</el-tab-pane>
					<el-tab-pane label="prompt" name="prompt">
						<div class="index-contain-left-content">
							<el-input type="textarea" :rows="11" placeholder="请输入内容" v-model="textarea">
							</el-input>
						</div>
					</el-tab-pane>
				</el-tabs>
				<div class="iclc-card">
					<el-button @click="upload">文件上传</el-button>
					<el-input class="iclc-file-input" v-model="link" placeholder="论文链接输入框"></el-input>
				</div>
				<el-button type="primary" @click="submit">提交</el-button>
			</div>
			<div class="index-contain-right">
				<p v-html="result"></p>
			</div>
		</div>
		<input v-show="false" id="files" type="file" />
		<Sliderbar />
	</div>
</template>
<script>
import api from '../../api';
import Sliderbar from '../../components/Sliderbar/Sliderbar.vue';
export default {
	name: 'Home',
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
			//上传文件
			fileName: "",
			top_p: 30,
			temperature: 30,
			//链接
			link: "",
			// 结果
			result: "",
			// 文本输入框
			textarea: '',
			// tab
			activeName: 'model',
			// 加载
			loading: false,
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
				//上传文件
				fileName: this.fileName,
				top_p: this.top_p / 100,
				temperature: this.temperature / 100,
				//链接
				link: this.link,
			};
			this.loading = true;
			api.requestPaperSummary(tmp_form)
				.then(res => {
					console.log(res);
					if (res.ret !== -1) {
						this.result = res.data;
					} else {
						throw new Error(res.msg || '提交失败');
					}

					this.$message({
						message: '提交成功',
						type: 'success'
					});
				})
				.catch(err => {
					console.log(err);
					this.$message.error(err.message || err.msg || '提交失败');
				})
				.finally(() => {
					this.loading = false;
				})
		},
		//触发上传
		upload() {
			document.getElementById("files").click();
		},
		//处理文件
		handleFiles() {
			var selectedFile = document.getElementById("files").files[0]; //获取读取的File对象
			console.log(selectedFile);
			const formData = new FormData();
			formData.append("file", selectedFile);
			this.loading = true;
			api.requestPaperUpload(formData)
				.then(res => {
					console.log(res);
					this.fileName = res.data.data;
					this.$message({
						message: "上传成功",
						type: "success",
					});
				})
				.catch(err => {
					console.log(err);
					this.$message.error("上传失败" + err);
				})
				.finally(() => {
					this.loading = false;
				})
		},
		handleClick(tab, event) {
			console.log(tab, event);
		}
	},
	components: {
		Sliderbar
	},
	mounted() {
		const inputElement = document.getElementById("files");
		inputElement.addEventListener("change", this.handleFiles, false);
	},
};
</script>
<style lang="scss" scoped>
@import "./Home.scss";
</style>