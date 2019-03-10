package me.lntu.lntuPro

import okhttp3.OkHttpClient
import okhttp3.Request


object Getscore {
    val client = OkHttpClient()
    var html: String? = null

    fun score(cookie: String) {
        val scoreUrl = "http://10.21.24.120:11182/newacademic/student/queryscore/queryscore.jsdo?groupId=&moduleId=2020"
        val request = Request.Builder()
            .url(scoreUrl)
            .header("Cookie", cookie)
            .build()
        try {
            client.newCall(request).execute().use { response ->
                html = response.body()!!.string()
            }
            println(html)
        } catch (e: Exception) {
            println("获取成绩失败..")
        }
    }

    fun parseHtml() {

    }
}