import axios from 'axios'
import qs from 'qs'
import {
	Message
} from 'element-ui'

axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';

const service = axios.create({
	baseURL: 'http://localhost:8000/api',
	timeout: 15000 
})

service.interceptors.request.use(config => {
	
	if(config.method === "post"){
		
		config.data = qs.stringify(config.data,  { indices: false });
	}
	
	return config;
}, error => {
	Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
	success => {

		if (success.data.code == 0) {

			return success.data;

		}else if (success.data.code == 1){

			return success.data;
		} else {

			Message({
				message: success.data.msg,
				type: 'error',
				center: true
			});
			return Promise.reject(success.data);
		}
	},
	error => {
		Message({
			message: '系统异常，请求中断',
			type: 'error',
			center: true
		});
		return Promise.reject(error);
	}
)

export default service
