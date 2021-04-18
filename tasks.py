from invoke import task


@task
def clean(ctx):
    res = ctx.run(
        "docker ps -a | egrep '(veos|spine|leaf)' | awk '{print($1)}'", hide=True
    )
    if res.ok and len(res.stdout) > 0:
        print("Deleting vrnetlab containers...")
        ctx.run(
            "xargs docker rm -f <<EOF\n{cont_uuids}\nEOF".format(cont_uuids=res.stdout)
        )
        print("\nAll vrnetlab containers have been removed.")
    else:
        print("Did not find any vrnetlab containers.")


@task
def deploy_lab(ctx):
    ctx.run("cd ansible && ansible-playbook provision_lab.yml")


@task
def configure_lab(ctx):
    ctx.run("cd ansible && ansible-playbook configure_lab.yml")


@task
def precheck(ctx):
    ctx.run("pre-commit run")


@task
def validate_lab(ctx):
    ctx.run("cd ansible && ansible-playbook validate_lab.yml")


@task
def test(ctx):
    ctx.run("pytest tests -v")
