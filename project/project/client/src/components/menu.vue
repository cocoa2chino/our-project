<template>
  <el-aside class="fater-left">
      <div class="fater-header-logo">抗疫物资管理系统</div>
      <el-menu :default-active="this.$router.currentRoute.path" 
        background-color="#6cc6cb" text-color="#F2f2f2" active-text-color="#eae5c9" router>
          <template v-for="(item, index) in menuList">
            <el-menu-item :key="index" :index="item.path">
                <span :class="item.icon"></span> 
                <span slot="title">{{ item.name }}</span>
            </el-menu-item>
          </template>
      </el-menu>
  </el-aside>
</template>

<style>
</style>

<script>

    export default{
      props: {
              menuList: []
      },
          
    }
</script>