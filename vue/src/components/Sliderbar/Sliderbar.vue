<template>
    <div class="sliderbar">
        <div class="sliderbar-content" @mouseover="showHover" @mouseout="hideHover">
            <i class="el-icon-phone-outline"></i>
            <p class="sliderbar-content-text">联系我们</p>
        </div>
        <div v-show="hoverValue" class="sliderbar-hover">
            <img class="sliderbar-hover-img" src="../../../public/image/WeChat.png"/>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Sliderbar',
    data() {
        return {
            hoverValue: false,
        }
    },
    methods: {
        showHover() {
            this.hoverValue = true;
        },
        hideHover() {
            this.hoverValue = false;
        }
    }
}
</script>

<style lang="scss" scoped>
@import "./Sliderbar.scss";
</style>