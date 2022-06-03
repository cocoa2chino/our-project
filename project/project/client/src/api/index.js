import http from "../utils/http.js";

/** 系统接口 */
export function login(param){
	
	return http.post('/login/', param);
}
export function exit(token){
	
	return http.get('/exit/', {params: token});
}
export function getLoginUser(token){
	
	return http.get('/info/', {params: {token: token}});
}
export function checkUserPwd(token, oldPwd){
	
	return http.get('/checkPwd/', {params: {token: token, oldPwd: oldPwd}});
}
export function updLoginUserInfo(params){
	
	return http.post('/info/', params);
}
export function updLoginUserPwd(token, newPwd){
	
	return http.post('/pwd/', {token: token, newPwd: newPwd});
}

/** 首页接口 */
export function getNoticeList(){
	
	return http.get('/notices/');
}
export function getTopTotal(){
	
	return http.get('/toptotal/');
}
export function getNowTotal(){
	
	return http.get('/nowtotal/');
}
export function getNow(){
	
	return http.get('/now/');
}

/** 用户信息接口 */
export function getPageUsers(pageIndex, pageSize, userName, name, phone){

	return http.get('/users/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, userName: userName, name: name, phone: phone}});
}
export function addUsers(params){
	
	return http.post('/users/add/', params);
}
export function updUsers(params){
	
	return http.post('/users/upd/', params);
}
export function delUsers(id){
	
	return http.post('/users/del/', {id: id});
}

/** 统计数据接口 */
export function getPageStatistics(pageIndex, pageSize, title){

	return http.get('/statistics/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, title: title}});
}
export function initStatistics(params){
	
	return http.post('/statistics/init/', params);
}

/** 通知信息接口 */
export function getPageNotices(pageIndex, pageSize, title){

	return http.get('/notices/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, title: title}});
}
export function addNotices(params){
	
	return http.post('/notices/add/', params);
}
export function updNotices(params){
	
	return http.post('/notices/upd/', params);
}
export function delNotices(id){
	
	return http.post('/notices/del/', {id: id});
}

/** 检查记录信息接口 */
export function getPageChecks(pageIndex, pageSize, token, resl, loc){

	return http.get('/check/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, token: token, resl: resl, loc: loc}});
}
export function addChecks(params){
	
	return http.post('/check/add/', params);
}
export function updChecks(params){
	
	return http.post('/check/upd/', params);
}
export function delChecks(id){
	
	return http.post('/check/del/', {id: id});
}

/** 异常记录信息接口 */
export function getPageAbnormitys(pageIndex, pageSize, token, name){

	return http.get('/abnormity/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, token: token, name: name}});
}
export function addAbnormitys(params){
	
	return http.post('/abnormity/add/', params);
}
export function updAbnormitys(params){
	
	return http.post('/abnormity/upd/', params);
}
export function delAbnormitys(id){
	
	return http.post('/abnormity/del/', {id: id});
}

/** 接种记录信息接口 */
export function getPageVaccinates(pageIndex, pageSize, token, name, card, phone, address){

	return http.get('/vaccinate/page/', 
        {params: {pageIndex: pageIndex, pageSize: pageSize, token: token, name: name, card: card, phone: phone, address: address}});
}
export function addVaccinates(params){
	
	return http.post('/vaccinate/add/', params);
}
export function updVaccinates(params){
	
	return http.post('/vaccinate/upd/', params);
}
export function delVaccinates(id){
	
	return http.post('/vaccinate/del/', {id: id});
}