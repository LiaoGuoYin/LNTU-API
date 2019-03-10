package me.lntu.lntuPro

import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request

class Login(private val username: String, private val password: String) {
    val client = OkHttpClient()
    var cookie: String? = null
    var html: String? = null

    init {
        initCookie()
        loginProcess()
    }

    fun initCookie() {
        val checkUrl = "http://10.21.24.120:11182/newacademic/common/security/check1.jsp"
        // val checkUrl = "http://202.199.224.121:11182/newacademic/common/security/check1.jsp"
        val request = Request.Builder()
            .url(checkUrl)
            .build()

        try {
            client.newCall(request).execute().use { response ->
                cookie = response.headers().values("Set-Cookie").get(0).substring(0, 47)
                println(cookie)
            }

        } catch (e: Exception) {
            println("获取Cookie失败")
            e.printStackTrace()
        }

    }

    fun loginProcess() {
        val loginUrl = "http://10.21.24.120:11182/newacademic/j_acegi_security_check"
        // val loginUrl = "http://202.199.224.121:11182/newacademic/j_acegi_security_check"
        println("login..")

        val formBody = FormBody.Builder()
            .add("j_username", username)
            .add("j_password", password)
            .build()

        val request = Request.Builder()
            .url(loginUrl)
            .addHeader("Cookie", cookie!!)
            .post(formBody)
            .build()

        try {
            client.newCall(request).execute().use { response ->
                html = response.body()!!.string()
            }
            // println("登陆成功: " + html)
        } catch (e: Exception) {
            println("学号或密码错误")
        }

    }

}