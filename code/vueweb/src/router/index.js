import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store';

import Login from '@/pages/client/Login';
import Backstage from '@/pages/client/Backstage'
import ChangeDetection from '@/pages/client/ChangeDetection'
import GroundObjectsClassification from '@/pages/client/GroundObjectsClassification'
import ObjectDetection from '@/pages/client/ObjectDetection'
import TargetExtraction from '@/pages/client/TargetExtraction'
import EditInfo from '@/pages/client/EditInfo'
import ErrorPage from '@/pages/ErrorPage'

/*
解决vue-router报NavigationDuplicated: Avoided redundant navigation to current location 的问题
避免到当前位置的冗余导航。 简单来说就是重复触发了同一个路由。
* */
// const original = Router.prototype.push
// Router.prototype.push = function push(location) {
//   return original.call(this, location).catch(err => err)
// }

Vue.use(Router)

let router = new Router({
    routes: [
        {
            path: "/",
            redirect: "/login"
        }, {
            path: '/login',
            name: 'Login',
            component: Login
        }, {
            path: '/backstage',
            name: 'Backstage',
            redirect: "/backstage/changeDetection",
            component: Backstage,
            children: [
                {
                    path: 'changeDetection',
                    name: 'ChangeDetection',
                    component: ChangeDetection,
                    meta: {
                        requireLogin: true,
                    },
                }, {
                    path: 'groundObjectsClassification',
                    name: 'GroundObjectsClassification',
                    component: GroundObjectsClassification,
                    meta: {
                        requireLogin: true,
                    },
                }, {
                    path: 'objectDetection',
                    name: 'ObjectDetection',
                    component: ObjectDetection,
                    meta: {
                        requireLogin: true,
                    },
                }, {
                    path: 'targetExtraction',
                    name: 'TargetExtraction',
                    component: TargetExtraction,
                    meta: {
                        requireLogin: true,
                    },
                }, {
                    path: 'editInfo',
                    name: 'EditInfo',
                    component: EditInfo,
                    meta: {
                        requireLogin: true,
                    },
                }
            ]
        }, {//404页面
            path: '*',
            name: 'ErrorPage',
            component: ErrorPage
        }
    ],
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return {x: 0, y: 0}
        }
    }
});

//登录拦截
router.beforeEach((to, from, next) => {
    if (to.meta.requireLogin) {
        if (store.state.clientId) {
            next()
        } else {
            next({
                path: '/login',
                query: {redirect: to.fullPath}
            })
        }
    } else {
        next();
    }
});

export default router;
