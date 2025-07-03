from chalice import Response


def health_routers(app, cors=None):
    @app.route("/health", methods=["GET"], cors=cors)
    def health_check():
        return Response(body={"status": "ok"})
