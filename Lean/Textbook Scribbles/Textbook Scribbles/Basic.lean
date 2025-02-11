-- def hello := "world"
-- /- Define some constants. -/

-- def m : Nat := 1       -- m is a natural number
-- def n : Nat := 0
-- def b1 : Bool := true  -- b1 is a Boolean
-- def b2 : Bool := false

-- /- Check their types. -/

-- #check m            -- output: Nat
-- #check n
-- #check n + 0        -- Nat
-- #check m * (n + 0)  -- Nat
-- #check b1           -- Bool
-- #check b1 && b2     -- "&&" is the Boolean and
-- #check b1 || b2     -- Boolean or
-- #check true         -- Boolean "true"

-- #check Nat               -- Type
-- #check Bool              -- Type
-- #check Nat → Bool        -- Type
-- #check Nat × Bool        -- Type
-- #check Nat → Nat         -- ...
-- #check Nat × Nat → Nat
-- #check Nat → Nat → Nat
-- #check Nat → (Nat → Nat)
-- #check Nat → Nat → Bool
-- #check (Nat → Nat) → Nat

-- def α : Type := Nat
-- def β : Type := Bool
-- def F : Type → Type := List
-- def G : Type → Type → Type := Prod

-- #check α        -- Type
-- #check F
-- #check F α      -- Type
-- #check F Nat    -- Type
-- #check G α      -- Type → Type
-- #check G α β    -- Type
-- #check G α Nat  -- Type

-- #check Type
-- #check Type 0

-- #check fun x : Nat => fun y : Bool => if not y then x + 1 else x + 2
-- #check fun (x : Nat) (y : Bool) => if not y then x + 1 else x + 2
-- #check fun x y => if not y then x + 1 else x + 2   -- Nat → Bool → Nat

-- #check let y := 2 + 2; y * y   -- Nat
-- #eval  let y := 2 + 2; y * y   -- 16

-- def twice_double (x : Nat) : Nat :=
--   let y := x + x; y * y

-- #eval twice_double 2   -- 16

-- def foo := let a := Nat; fun x : a => x + 2

-- --def bar := (fun a => fun x : a => x + 2) Nat

-- variable (α β γ : Type)
-- variable (g : β → γ) (f : α → β) (h : α → α)
-- variable (x : α)

-- def compose := g (f x)
-- def doTwice := h (h x)
-- def doThrice := h (h (h x))

-- #print compose
-- #print doTwice
-- #print doThrice

-- #check List.nil
-- #check List.cons
-- #check List.map

-- namespace Foo
--   def a : Nat := 5
--   def f (x : Nat) : Nat := x + 7

--   def fa : Nat := f a
-- end Foo

-- #check Foo.a
-- #check Foo.f

-- namespace Foo
--   def ffa : Nat := f (f a)
-- end Foo

-- #check Foo.a

-- universe u v

-- def f (α : Type u) (β : α → Type v) (a : α) (b : β a) : (a : α) × β a :=
--   ⟨a, b⟩

-- def g (α : Type u) (β : α → Type v) (a : α) (b : β a) : Σ a : α, β a :=
--   Sigma.mk a b

-- def h1 (x : Nat) : Nat :=
--   (f Type (fun α => α) Nat x).2

-- #eval h1 5 -- 5

-- def h2 (x : Nat) : Nat :=
--   (g Type (fun α => α) Nat x).2

-- #eval h2 5 -- 5

universe u
def Lst (α : Type u) : Type u := List α
def Lst.cons (α : Type u) (a : α) (as : Lst α) : Lst α := List.cons a as
def Lst.nil (α : Type u) : Lst α := List.nil
def Lst.append (α : Type u) (as bs : Lst α) : Lst α := List.append as bs
#check Lst          -- Type u_1 → Type u_1
#check Lst.cons     -- (α : Type u_1) → α → Lst α → Lst α
#check Lst.nil      -- (α : Type u_1) → Lst α
#check Lst.append   -- (α : Type u_1) → Lst α → Lst α → Lst α
#check Lst.cons Nat 0 (Lst.nil Nat)
#eval Lst.cons Nat 0 (Lst.nil Nat)

def as : Lst Nat := Lst.nil Nat
def bs : Lst Nat := Lst.cons Nat 5 (Lst.nil Nat)

#check Lst.append Nat as bs
#eval Lst.append Nat as bs

variable {p : Prop}
variable {q : Prop}
theorem t1 : p → q → p :=
  fun hp : p =>
  fun hq : q =>
  show p from hp
