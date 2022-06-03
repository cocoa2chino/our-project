import {getLoginUser} from "../api";

// 系统管理员
export const adminMenus = {
    path: '/home',
    name: 'home',
    component: require("../views/home.vue").default,
    children: [
        {
            path: '/index',
            name: '系统首页',
            icon: "fa fa-home",
            component: require("../views/pages/index.vue").default
        },
        {
            path: '/users',
            name: '用户管理',
            icon: "fa fa-address-book-o",
            component: require("../views/pages/users.vue").default
        },
        {
            path: '/vaccinateLogs',
            name: '物资管理',
            icon: "fa fa-address-card",
            component: require("../views/pages/vaccinateLogs.vue").default
        },
        {
            path: '/checkLogs',
            name: '入出库记录管理',
            icon: "fa fa-sliders",
            component: require("../views/pages/checkLogs.vue").default
        },
        {
            path: '/notices',
            name: '求助信息管理',
            icon: "fa fa-bullhorn",
            component: require("../views/pages/notices.vue").default
        },
        {
            path: '/statistics',
            name: '统计数据管理',
            icon: "fa fa-bug",
            component: require("../views/pages/statistics.vue").default
        }
    ]
};

export const userMenus = {
    path: '/home',
    name: 'home',
    component: require("../views/home.vue").default,
    children: [
        {
            path: '/index',
            name: '系统首页',
            icon: "fa fa-home",
            component: require("../views/pages/index.vue").default
        },
        {
            path: '/notices',
            name: '求助信息管理',
            icon: "fa fa-bullhorn",
            component: require("../views/pages/notices.vue").default
        },
        {
            path: '/statistics',
            name: '统计数据管理',
            icon: "fa fa-bug",
            component: require("../views/pages/statistics.vue").default
        }
    ]
};

export default function initMenu(router, store){
	
    let token = null;
    if(store.state.token){

        token = store.state.token;
    }else{

        token = sessionStorage.getItem("token");
        store.state.token = sessionStorage.getItem("token");
    }

    getLoginUser(token).then(resp =>{

        if(resp.data.type == 0){
            router.addRoute(adminMenus);
            store.commit("setMenus", adminMenus);
        }
    
        if(resp.data.type == 1){
            router.addRoute(userMenus);
            store.commit("setMenus", userMenus);
        }
    });
}




