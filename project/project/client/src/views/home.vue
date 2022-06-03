<template>
    <el-container>
        <Menu :menuList="this.$store.state.menus.children"></Menu>
        <el-container>
            <Nav></Nav>
            <el-main class="fater-body">
                <el-breadcrumb v-if="this.$router.currentRoute.path != '/index' " class="fater-body-breadcrumb">
                    <el-breadcrumb-item>
                        <el-breadcrumb-item :to="{ path: '/index' }"><strong>系统首页</strong></el-breadcrumb-item>
                    </el-breadcrumb-item>
                    <el-breadcrumb-item><strong>{{ this.$router.currentRoute.name }}</strong></el-breadcrumb-item>
                </el-breadcrumb>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<style>

</style>

<script>
    import Nav from "../components/nav.vue";
    import Menu from "../components/menu.vue";

    export default{
        
        data(){

            return {
                
            }
        },
        methods: {

        },
        components: {
            Nav,
            Menu
        }
    }
</script>