import { fetchApi } from "../utils/axios";
import host from '../utils/host';

export default {
	requestPaperSummary(data) {
		return fetchApi({
			url: `${host}/api/request_paper_summary`,
			method: 'POST',
			data,
		});
	},
	requestPaperUpload(data) {
		return fetchApi({
			url: `${host}/api/request_paper_upload`,
			method: 'POST',
			data,
			headers: {
				"Content-type": "multipart/form-data",
			}
		})
	}
}