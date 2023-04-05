import axios from 'axios';
import host from './host';
function AJAXError(name, message, code) {
	this.name = name || 'apiError';
	this.code = code || -1;
	this.message = message || '系统异常，请稍后重试';
	this.stack = new Error().stack;
}

AJAXError.prototype = new Error();

export function fetchApi(option) {
	let { url } = option;
	// const purePath = url.indexOf('?') > 0 ? url.slice(0, url.indexOf('?')) : url;
	const axiosAttribute = {
		url,
		baseURL: host,
		method: (option.method || 'GET').toUpperCase(),
		withCredentials:
			option.withCredentials !== undefined ? option.withCredentials : true,
		crossDomain: true,
		xDomain: true,
		timeout: option.timeout || 6000,
	}

	if (axiosAttribute.method === 'POST') {
		axiosAttribute.data = option.data;
	} else if (axiosAttribute.method === 'GET') {
		axiosAttribute.params = option.params;
	}

	if (option.headers) {
		axiosAttribute.headers = { ...option.headers, ...axiosAttribute.headers };
	}

	return axios(axiosAttribute)
		.then(res => {
			const { data } = res;
			if (!data) {
				throw new AJAXError();
			}
			return data;
		})
		.catch(error => {
			const httpError = new AJAXError('httpError');
			if (error.response) {
				httpError.code = error.response.status;
				httpError.message = error.response.statusText;
			} else if (error.request) {
				httpError.message = '请求超时';
			} else {
				httpError.message = error.message;
			}

			throw error;
		})
}
